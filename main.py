import json
from typing import Optional, Annotated

from fastapi import FastAPI, Depends, HTTPException
#from sqlmodel import Session, create_engine

from sqlalchemy import select, create_engine
from sqlalchemy.orm import Session

from api.models.ControlsResponse import ControlsResponse
from api.models.DataTypeTagCreationData import DataTypeTagCreationData
from api.models.DataTypeTagResponse import DataTypeTagResponse
from api.models.DatabaseMetadataAdapterResponse import DatabaseMetadataAdapterResponse
from api.models.MySQLDatabaseMetadataAdapterCreationData import MySQLDatabaseMetadataAdapterCreationData

from api.models.RegExOnFieldNameControlCreationData import RegExOnFieldNameControlCreationData
from internal.models.Control import Control
from internal.models.DataTypeTag import DataTypeTag
from internal.models.DatabaseMetadataAdapter import DatabaseMetadataAdapter
from internal.models.MySQLDatabaseMetadataAdapter import MySQLDatabaseMetadataAdapter
from internal.models.RegExOnFieldNameControl import RegExOnFieldNameControl

engine = create_engine("mysql+pymysql://root@127.0.0.1/challengeML")

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

@app.get("/api/v1/tags", response_model=list[DataTypeTagResponse])
async def getDataTypeTags(session: SessionDep):
    tags = session.scalars(
        select(DataTypeTag)
    ).all()

    return tags

@app.post("/api/v1/tags", response_model=DataTypeTagResponse)
async def addDataTypeTag(data: DataTypeTagCreationData, session: SessionDep):
    newTag = DataTypeTag(name=data.name, description=data.description)
    session.add(newTag)
    session.commit()
    session.refresh(newTag)

    return newTag


@app.get("/api/v1/controls", response_model=list[ControlsResponse])
async def getControls(session: SessionDep):
    controls = session.scalars(
        select(Control)
    ).all()

    return controls

@app.post("/api/v1/controls/regexOnFieldName", response_model=ControlsResponse)
async def addControlRegExOnFieldName(data: RegExOnFieldNameControlCreationData, session: SessionDep):
    mappedTags = None
    try:
        mappedTags = data.parsedAffectedTags(session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    newControl = RegExOnFieldNameControl(
        name=data.name,
        affectedTags=mappedTags,
        regex=data.regex
    )
    session.add(newControl)
    session.commit()
    session.refresh(newControl)

    return newControl

@app.get("/api/v1/databases", response_model=list[DatabaseMetadataAdapterResponse])
async def getDatabases(session: SessionDep):
    databases = session.scalars(
        select(DatabaseMetadataAdapter)
    ).all()

    return databases

@app.post("/api/v1/databases/mysql", response_model=DatabaseMetadataAdapterResponse)
async def createMySQLDatabase(data: MySQLDatabaseMetadataAdapterCreationData, session: SessionDep) -> DatabaseMetadataAdapterResponse:
    newDatabase = MySQLDatabaseMetadataAdapter(
        host=data.host, 
        port=data.port,
        username=data.username,
        password=data.password
    )
    session.add(newDatabase)
    session.commit()
    session.refresh(newDatabase)
    return newDatabase

@app.post("/api/v1/databases/{id}/scan")
async def scanDatabase(id: int, session: SessionDep):
    database = session.scalars(
        select(DatabaseMetadataAdapter)
        .where(DatabaseMetadataAdapter.id == id)
    ).first()
    
    if database is None:
        raise HTTPException(status_code=400, detail="The selected database does not exist or was disabled")
    
    controls = session.scalars(
        select(Control)
    ).all()
    
    structure = database.getStructure()
    for schema in structure:
        schema.run(controls)
    
    session.add(database)
    session.commit()