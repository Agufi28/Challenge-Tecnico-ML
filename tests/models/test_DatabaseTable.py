import pytest
from internal.models.DatabaseTable import DatabaseTable
from internal.models.DatabaseField import DatabaseField
from internal.models.Control import Control
from unittest.mock import MagicMock

def testDatabaseTableCreation(session, makeSchema):
    schema = makeSchema()
    table = DatabaseTable(name="Test Table")
    table.schema_id = schema.id
    session.add(table)
    session.commit()

    persisted_table = session.query(DatabaseTable).filter_by(name="Test Table").first()
    assert persisted_table is not None
    assert persisted_table.name == "Test Table"
    assert persisted_table.fields == []

def testDatabaseTableAddField(session, makeSchema, makeField):
    schema = makeSchema()
    table = DatabaseTable(name="Test Table")
    table.schema_id = schema.id
    field = makeField(name="Test Field")
    table.addField(field)

    session.add(table)
    session.commit()

    persisted_table = session.query(DatabaseTable).filter_by(name="Test Table").first()
    assert persisted_table is not None
    assert len(persisted_table.fields) == 1
    assert persisted_table.fields[0].name == "Test Field"

def testDatabaseTableGetFields(session, makeSchema, makeField):
    schema = makeSchema()
    table = DatabaseTable(name="Test Table")
    table.schema_id = schema.id
    field1 = makeField(name="Field 1")
    field2 = makeField(name="Field 2")
    table.addField(field1)
    table.addField(field2)

    session.add(table)
    session.commit()

    persisted_table = session.query(DatabaseTable).filter_by(name="Test Table").first()
    assert persisted_table is not None
    fields = persisted_table.getFields()
    assert len(fields) == 2
    assert fields[0].name == "Field 1"
    assert fields[1].name == "Field 2"
