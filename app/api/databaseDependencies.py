from typing import Annotated
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from internal.secrets.Secrets import Secrets


engine = create_engine(
    f"mysql+pymysql://{Secrets.getDatabaseUser()}:{Secrets.getDatabasePassword()}@{Secrets.getDatabaseHost()}:{Secrets.getDatabasePort()}/{Secrets.getDatabaseName()}"
)

def getDbSession():
    with Session(engine) as session:
        yield session

DBSessionDep = Annotated[Session, Depends(getDbSession)]
