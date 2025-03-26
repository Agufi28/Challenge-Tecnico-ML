from fastapi import APIRouter, HTTPException
from loguru import logger

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from internal.models.DatabaseMetadataAdapter import DatabaseMetadataAdapter
from internal.models.MySQLDatabaseMetadataAdapter import MySQLDatabaseMetadataAdapter
from internal.models.DatabaseSchema import DatabaseSchema
from internal.models.DatabaseTable import DatabaseTable
from internal.models.DatabaseField import DatabaseField
from internal.models.FieldTag import FieldTag
from internal.models.Control import Control
from internal.models.ScanResult import ScanResult

from api.models.Databases import DatabaseMetadataAdapterResponse, MySQLDatabaseMetadataAdapterCreationData
from api.models.Scans import ScanDatabaseResponse

from api.auth.authorizationDependencies import AuthenticatedUserDep
from api.databaseDependencies import DBSessionDep


router = APIRouter(prefix="/api/v1/databases")


@router.get(
    "/", 
    summary="Get all the available databases",
    response_model=list[DatabaseMetadataAdapterResponse], 
    tags=["Non-Admin endpoints"]
)
async def getDatabases(session: DBSessionDep, user: AuthenticatedUserDep):
    databases = session.scalars(
        select(DatabaseMetadataAdapter)
    ).all()

    logger.debug(f"the user {user.username} accessed the endpoint [GET /api/v1/databases]")
    return databases


@router.post(
    "/mysql", 
    summary="Add a new MySQL type database to be available for scanning",
    response_model=DatabaseMetadataAdapterResponse, 
    tags=["Non-Admin endpoints"]
)
async def createMySQLDatabase(data: MySQLDatabaseMetadataAdapterCreationData, session: DBSessionDep, user: AuthenticatedUserDep) -> DatabaseMetadataAdapterResponse:
    newDatabase = MySQLDatabaseMetadataAdapter(
        host=data.host, 
        port=data.port,
        username=data.username,
        password=data.password,
        createdBy=user
    )
    session.add(newDatabase)
    session.commit()
    session.refresh(newDatabase)

    logger.info(f"the user [{user.username}] added a new database to the system. dabase id={newDatabase.id}")
    return newDatabase


@router.post(
    "/{id}/scans",
    summary="Trigger the scan process for the database with  id = {id}",
    response_model=ScanDatabaseResponse,
    tags=["Non-Admin endpoints"]
)
async def scanDatabase(id: int, session: DBSessionDep, user: AuthenticatedUserDep):
    database = session.scalars(
        select(DatabaseMetadataAdapter)
        .where(DatabaseMetadataAdapter.id == id)
    ).first()
    
    if database is None:
        raise HTTPException(status_code=400, detail="The selected database does not exist or was disabled")

    controls = session.scalars(
        select(Control)
    ).all()
    
    scan = database.scanStructure(requestedBy=user, dataSampleSize=10)
    database.runControlsOnLastScan(controls)

    session.add(database)
    session.commit()

    logger.info(f"the user [{user.username}] requested a new scan for the database with id={database.id}")
    return scan


@router.get(
    "/{id}/scans",
    summary="Get the past scans of the database with id = {id}",
    tags=["Non-Admin endpoints"]
)
async def getDatabaseResults(id: int, session: DBSessionDep, user: AuthenticatedUserDep):
    database = session.execute(
        select(ScanResult.id, ScanResult.executed_on)
        .where(ScanResult.database_id == id)
    ).mappings().all()

    logger.debug(f"the user {user.username} accessed the scan history for the database with id={id}")
    return database


@router.get(
    "/{id}/scans/last",
    summary="Get the results of the last scan on the database with id = {id}",
    tags=["Non-Admin endpoints"]
)
async def getDatabaseResults(id: int, session: DBSessionDep, user: AuthenticatedUserDep):
    database = session.scalars(
        select(ScanResult)
        .where(ScanResult.database_id == id)
        .order_by(ScanResult.id.desc())
        .options(
            joinedload(ScanResult.schemas)
            .subqueryload(DatabaseSchema.tables)
            .subqueryload(DatabaseTable.fields)
            .subqueryload(DatabaseField.tags)
            .subqueryload(FieldTag.tag)
        )
    ).first()

    logger.debug(f"the user {user.username} accessed the last scan results for the database with id={id}")
    return database


@router.get(
    "/scans/{id}",
    summary="Get the database scan result with id = {id}. Note the id is the scan's, not the database's",
    tags=["Non-Admin endpoints"]
)
async def getDatabaseResults(id: int, session: DBSessionDep, user: AuthenticatedUserDep):
    database = session.scalars(
        select(DatabaseSchema)
        .where(DatabaseSchema.scan_id == id)
        .options(
            joinedload(DatabaseSchema.tables)
            .subqueryload(DatabaseTable.fields)
            .subqueryload(DatabaseField.tags)
            .subqueryload(FieldTag.tag)
        )
    ).first()

    logger.debug(f"the user {user.username} accessed scan results with id={id}")
    return database