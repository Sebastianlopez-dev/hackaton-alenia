"""Statement-level read-only classification.

This is a guard rail for the approval message and the SQL capability, not a
security boundary: the boundary is the credential and the warehouse
permission used to connect. It catches the obvious case of a model that
emits a statement able to write.
"""

import pytest

from hackaton_alenia.sql_guard import is_read_only

READ_ONLY = [
    "SELECT LOCALCODE, CLASSID, SUBSIDIARYCODE, HOLDINGID FROM MD_LOCALVALUE_T WHERE LOCALCODE = 'ABC'",
    "select 1",
    "WITH recent AS (SELECT * FROM MD_LOCALVALUEHISTORY_T) SELECT * FROM recent",
    "SELECT 1;",
    "  \n SELECT 1 \n ",
]

A_BLE_TO_WRITE = [
    "INSERT INTO MD_LOCALVALUE_T VALUES (1)",
    "UPDATE MD_LOCALVALUE_T SET HOLDINGID = 'H_NEW'",
    "DELETE FROM MD_LOCALVALUE_T",
    "MERGE INTO MD_LOCALVALUE_T USING source ON 1 = 1",
    "DROP TABLE MD_LOCALVALUE_T",
    "ALTER TABLE MD_LOCALVALUE_T ADD COLUMN X INT",
    "TRUNCATE TABLE MD_LOCALVALUE_T",
    "CREATE TABLE X (A INT)",
    "GRANT SELECT ON MD_LOCALVALUE_T TO someone",
    "SELECT 1; DELETE FROM MD_LOCALVALUE_T",
    "",
]


@pytest.mark.parametrize("statement", READ_ONLY)
def test_a_single_read_statement_is_read_only(statement):
    assert is_read_only(statement) is True


@pytest.mark.parametrize("statement", A_BLE_TO_WRITE)
def test_a_statement_able_to_write_is_never_read_only(statement):
    assert is_read_only(statement) is False
