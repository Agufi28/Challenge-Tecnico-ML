import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from internal.models.Base import Base
from internal.models.DatabaseField import DatabaseField
from internal.models.DataTypeTag import DataTypeTag
from internal.models.FieldDataTypes import FieldDataTypes
from internal.models.RegExOnFieldNameControl import RegExOnFieldNameControl
from internal.models.DatabaseTable import DatabaseTable
from internal.models.DatabaseSchema import DatabaseSchema
from internal.models.ScanResult import ScanResult
from internal.models.MySQLDatabaseMetadataAdapter import MySQLDatabaseMetadataAdapter

@pytest.fixture
def emailDataTypeTag():
    tag = DataTypeTag("EMAIL")
    tag.id = 1
    return tag

@pytest.fixture
def usernameTag():
    tag = DataTypeTag("USERNAME")
    tag.id = 2
    return tag 

@pytest.fixture
def affectedTags(emailDataTypeTag):
    return {emailDataTypeTag: 10}

@pytest.fixture
def regex():
    return r"email|e_?mail"

@pytest.fixture
def control(affectedTags, regex):
    return RegExOnFieldNameControl("Test Control", affectedTags, regex)

@pytest.fixture
def schema(tables = []):
    return DatabaseSchema("test_schema", tables)

@pytest.fixture(name="makeScanResult")
def makeScanResult(session):
    scanResult = ScanResult(MySQLDatabaseMetadataAdapter("host", "user", "password", "database"))
    session.add(scanResult)
    session.commit()
    return scanResult

@pytest.fixture(name="makeSchema")
def makeSchema(session, makeScanResult):
    def _make_schema(tables=[]):
        schema = DatabaseSchema("test_schema", tables)
        schema.scan_id = makeScanResult.id
        session.add(schema)
        session.commit()
        return schema
    return _make_schema

@pytest.fixture(name="makeTable")
def makeTable(session, makeSchema, fields=[]):
    def _make_table(fields=[]):
        table = DatabaseTable("test_table", fields)
        schema = makeSchema([table])
        session.add(table)
        session.commit()
        return schema.tables[0]
    return _make_table

@pytest.fixture(name="makeField")
def makeField(session, makeTable):
    def _make_field(name="test_field", field_type=FieldDataTypes.STRING):
        field = DatabaseField(name, field_type)
        table = makeTable([field])
        field.table_id = table.id
        session.add(field)
        session.commit()
        return field
    return _make_field

@pytest.fixture
def databaseMetadataAdapter():
    return MySQLDatabaseMetadataAdapter("host", "user", "password", "database")

@pytest.fixture
def scanResult(databaseMetadataAdapter):
    return ScanResult(databaseMetadataAdapter)

@pytest.fixture(name="session")
def dbSession():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = Session(engine)
    yield session
    session.rollback()
    session.close()