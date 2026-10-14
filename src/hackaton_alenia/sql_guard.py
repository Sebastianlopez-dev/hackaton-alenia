"""Statement-level read-only classification.

This is a guard rail for the approval message and the SQL capability, not a
security boundary. The real boundary is the credential and the warehouse
permission used to connect; this only catches the obvious case of a model
that emits a statement able to write.

It errs towards refusing: a statement it cannot recognise as a single read
is reported as not read-only, so the human sees the warning instead of a
false reassurance.
"""

import re

READERS = frozenset({"select", "with"})

WRITERS = frozenset({
    "alter", "copy", "create", "delete", "drop", "grant", "insert", "into",
    "merge", "optimize", "overwrite", "revoke", "truncate", "update",
    "upsert", "vacuum",
})

_LITERAL = re.compile(r"'[^']*'")
_WORD = re.compile(r"[a-z_][a-z_0-9]*")


def read_only_reason(statement: str) -> str | None:
    """Return why a statement is not a single read, or None when it is."""
    text = (statement or "").strip()
    if not text:
        return "the statement is empty"
    while text.endswith(";"):
        text = text[:-1].rstrip()
    if not text:
        return "the statement is empty"
    if ";" in text:
        return "the statement contains more than one statement"
    words = _WORD.findall(_LITERAL.sub("''", text).lower())
    if not words or words[0] not in READERS:
        return f"the statement starts with '{words[0] if words else ''}', which is not a read"
    written = WRITERS.intersection(words)
    if written:
        return f"the statement contains '{sorted(written)[0]}', which can write"
    return None


def is_read_only(statement: str) -> bool:
    """True only for a statement recognised as a single read."""
    return read_only_reason(statement) is None
