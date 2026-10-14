"""Deterministic UC1 orchestration with a labelled source for every step.

The script owns the structure: read the ticket, route it, retrieve
precedents, investigate, resolve, comment and set the status, always in that
order. The model only routes, proposes the next read-only query or says it
is done, and writes the resolution, all as JSON text, so the run never
depends on the model's tool calling.

Every protected action goes through the same capabilities as the agent flow
(``tools.ticket_tools``): one read-only guard, one approval gate, one audit
ledger. Each event carries its source:

- ``script``: deterministic code in this module
- ``agent``: text produced by the model
- ``human``: an approval decision
- ``service``: data returned by Databricks or OpenProject
"""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal

from langsmith import tracing_context

from hackaton_alenia.approvals import ApprovalDenied
from hackaton_alenia.llm import Resolution, abstention, classify_ticket, propose_next_step, write_resolution
from hackaton_alenia.sql_guard import read_only_reason
from hackaton_alenia.tools import ticket_tools

Source = Literal["script", "agent", "human", "service"]
SOURCES: tuple[Source, ...] = ("script", "agent", "human", "service")

MAX_QUERIES = 8


@dataclass(frozen=True)
class StatusNames:
    """Ticket statuses the script chooses between. Official names are still unverified."""

    proposal: str
    review: str


def run_pipeline(ticket_id, services, model, gate, *, statuses: StatusNames,
                 emit: Callable[[dict], None] | None = None, max_queries: int = MAX_QUERIES) -> dict:
    with tracing_context(enabled=False):
        return _Pipeline(ticket_id, services, model, gate, statuses, emit, max_queries).run()


class _Pipeline:
    def __init__(self, ticket_id, services, model, gate, statuses, emit, max_queries):
        self.ticket_id = ticket_id
        self.services = services
        self.model = model
        self.gate = gate
        self.statuses = statuses
        self.emit = emit
        self.max_queries = max_queries
        self.trace: list[dict] = []
        tools_by_origin = {origin: {tool.name: tool for tool in ticket_tools(services, gate, ticket_id, origin)}
                           for origin in ("agent", "script")}
        self.agent_tools = tools_by_origin["agent"]
        self.script_tools = tools_by_origin["script"]

    def event(self, step: str, source: Source, summary: str) -> None:
        record = {"step": step, "source": source, "summary": summary}
        self.trace.append(record)
        if self.emit:
            self.emit(record)

    def run(self) -> dict:
        ticket = self.services.read_ticket(self.ticket_id)
        self.event("read_ticket", "service", f"Ticket {ticket.id}: {ticket.title}")

        try:
            routing = classify_ticket(self.model, ticket)
        except ValueError:
            self.event("routing", "script", "The model did not return a valid routing; nothing was investigated")
            return self.result(None, abstention("The model did not return a valid routing"))
        context = routing.model_dump(by_alias=True)
        self.event("routing", "agent", f"{routing.use_case} / {routing.priority}; context {_context(routing)}")
        if hasattr(self.gate, "set_context"):
            self.gate.set_context(ticket_id=ticket.id, use_case=routing.use_case, priority=routing.priority)
        if routing.use_case != "UC1":
            self.event("routing", "script", f"{routing.use_case} is outside the UC1 pipeline; nothing was investigated")
            return self.result(routing, abstention(f"{routing.use_case} is not covered by the UC1 pipeline"))

        query = " ".join(part for part in (ticket.title, routing.affected_local_code, routing.class_id,
                                           routing.subsidiary) if part)
        self.event("precedents", "script", f"Searching precedents for: {query}")
        precedents = self.agent_tools["retrieve_similar_tickets"].invoke({"query": query})
        self.event("precedents", "service", _summarise(precedents, "precedent"))

        evidence = self.investigate(ticket, context, precedents)

        resolution = write_resolution(self.model, {
            "ticket": ticket.model_dump(), "routing": context, "precedents": precedents, "evidence": evidence})
        if resolution is None:
            self.event("resolution", "script", "The model did not return a valid resolution; abstaining")
            resolution = abstention("The model did not return a valid resolution")
        else:
            self.event("resolution", "agent", _describe(resolution))

        self.publish(ticket.id, resolution)
        return self.result(routing, resolution)

    def investigate(self, ticket, context, precedents) -> list[dict]:
        evidence: list[dict] = []
        for _ in range(self.max_queries):
            step = propose_next_step(self.model, {
                "ticket": ticket.model_dump(), "routing": context, "precedents": precedents, "evidence": evidence})
            if step is None:
                self.event("investigate", "script", "The model did not return a valid next step; investigation stops")
                return evidence
            if step.done:
                self.event("investigate", "agent", f"Investigation complete after {len(evidence)} step(s)")
                return evidence
            self.event("investigate", "agent", f"Proposed SQL: {step.sql} (purpose: {step.purpose})")
            reason = read_only_reason(step.sql)
            if reason:
                self.event("investigate", "script", f"Refused before approval: not a single read ({reason})")
                evidence.append({"sql": step.sql, "error": f"refused: not a single read ({reason})"})
                continue
            rows = self.protected(self.agent_tools["query_sql"], {"sql": step.sql, "purpose": step.purpose}, "investigate")
            evidence.append({"sql": step.sql, "purpose": step.purpose, "result": rows})
        self.event("investigate", "script", f"Query limit of {self.max_queries} reached; investigation stops")
        return evidence

    def publish(self, ticket_id: int, resolution: Resolution) -> None:
        text = render_comment(resolution)
        self.event("comment", "script", "Comment composed from the resolution")
        self.protected(self.script_tools["create_comment"], {"ticket_id": ticket_id, "text": text}, "comment")
        if resolution.proposed_correction:
            status, why = self.statuses.proposal, "a correction was proposed"
        else:
            status, why = self.statuses.review, "no correction could be proposed"
        self.event("status", "script", f"Status '{status}' chosen because {why}")
        self.protected(self.script_tools["update_status"], {"ticket_id": ticket_id, "status": status}, "status")

    def protected(self, tool, args: dict, step: str):
        """Run one approved capability and label the human decision and the service answer."""
        try:
            outcome = tool.invoke(args)
        except ApprovalDenied:
            self.event(step, "human", "Rejected; the run stops and nothing more is executed")
            raise
        self.event(step, "human", "Approved")
        self.event(step, "service", _summarise(outcome, "row"))
        return outcome

    def result(self, routing, resolution: Resolution) -> dict:
        return {
            "flow": "pipeline",
            "routing": routing.model_dump(by_alias=True) if routing else None,
            "resolution": resolution.model_dump(),
            "trace": self.trace,
        }


def render_comment(resolution: Resolution) -> str:
    """Deterministic comment text; the content comes from the model's resolution."""
    lines = ["UC1 analysis", "", resolution.analysis or "(no analysis)"]
    if resolution.proposed_correction:
        lines += ["", f"Proposed correction: {resolution.proposed_correction}"]
    if resolution.abstention_reason:
        lines += ["", f"No correction proposed: {resolution.abstention_reason}"]
    if resolution.evidence:
        lines += ["", "Evidence:"] + [f"- {item.source}: {item.detail}" for item in resolution.evidence]
    lines += ["", f"Confidence: {resolution.confidence}",
              "Generated by the UC1 pipeline: analysis by the model, wording by the script, approved by a human."]
    return "\n".join(lines)


def _context(routing) -> str:
    parts = {"subsidiary": routing.subsidiary, "class": routing.class_id, "local code": routing.affected_local_code}
    known = [f"{name} {value}" for name, value in parts.items() if value]
    return ", ".join(known) if known else "none extracted"


def _describe(resolution: Resolution) -> str:
    if resolution.proposed_correction:
        return f"Proposal ({resolution.confidence} confidence): {resolution.proposed_correction}"
    return f"No proposal: {resolution.abstention_reason or 'no reason given'}"


def _summarise(outcome, noun: str) -> str:
    if isinstance(outcome, dict) and "error" in outcome:
        return f"Error: {outcome['error']}"
    if isinstance(outcome, list):
        return f"{len(outcome)} {noun}{'' if len(outcome) == 1 else 's'} returned"
    return "Done"
