from typing import Optional, Annotated

from fastapi import FastAPI, Depends
#from sqlmodel import Session, create_engine

from sqlalchemy import select, create_engine
from sqlalchemy.orm import Session

from internal.models.DatabaseMetadataAdapter import DatabaseMetadataAdapter
from internal.models.MySQLDatabaseMetadataAdapter import MySQLDatabaseMetadataAdapter
from api.models.APIDatabaseSchema import APIDatabaseSchema

engine = create_engine("mysql+pymysql://root@127.0.0.1/challengeML")

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()

@app.get("/api/v1/databases")
async def getDatabases(session: SessionDep):
    data = [record._mapping for record in session.execute(select(DatabaseMetadataAdapter)).all()]
    print(data)
    return data

@app.post("/api/v1/databases/mysql", response_model=None)
async def createMySQLDatabase(session: SessionDep) -> DatabaseMetadataAdapter:
    database = MySQLDatabaseMetadataAdapter("testHost", 1234, "testUser", "testPW")
    session.add(database)
    session.commit()
    session.refresh(database)
    return database
