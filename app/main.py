from datetime import timedelta
import sys
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger

logger.remove()
logger.add("logs/DatabaseClasificationAPI_{time}.log",rotation="w6",format="{time:DD/MM/YYYY HH:mm:ss} - {level} - {message}")
logger.add(sys.stdout, colorize=True, format="<level>{time:DD/MM/YYYY HH:mm:ss} - {level} - {message}</level>")

from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException

from sqlalchemy import select, create_engine
from sqlalchemy.orm import joinedload

from internal.models.Control import Control
from internal.models.DataTypeTag import DataTypeTag
from internal.models.DatabaseField import DatabaseField
from internal.models.DatabaseMetadataAdapter import DatabaseMetadataAdapter
from internal.models.DatabaseSchema import DatabaseSchema
from internal.models.DatabaseTable import DatabaseTable
from internal.models.FieldTag import FieldTag
from internal.models.MySQLDatabaseMetadataAdapter import MySQLDatabaseMetadataAdapter
from internal.models.RegExOnFieldNameControl import RegExOnFieldNameControl
from internal.models.ScanResult import ScanResult
from internal.models.User import User


from api.models.ControlsResponse import ControlsResponse
from api.models.DataTypeTagCreationData import DataTypeTagCreationData
from api.models.DataTypeTagResponse import DataTypeTagResponse
from api.models.DatabaseMetadataAdapterResponse import DatabaseMetadataAdapterResponse
from api.models.MySQLDatabaseMetadataAdapterCreationData import MySQLDatabaseMetadataAdapterCreationData
from api.models.RegExOnFieldNameControlCreationData import RegExOnFieldNameControlCreationData
from api.models.ScanDatabaseResponse import ScanDatabaseResponse
from api.models.UserCreation import UserData, UserCreationData

from api.auth.JWTModels import Token
from api.auth.helperFunctions import createAccessToken, validateUserCredentialsAndGetUser

from api.databaseDependencies import DBSessionDep
from api.auth.authorizationDependencies import AuthenticatedUserDep, AuthenticatedAdminDep

app = FastAPI(
    title="Database clasification API",
    summary="This API was developed as part of the technical for the Cybersecurity Engineer position",
    contact={
        "name": "My github profile",
        "url": "https://github.com/Agufi28"
    }
)



@app.post(
    "/token",
    summary="Start a new API session and get a JWT bearer token",
    tags=["Session endpoints"]
)
async def processLoginAndGetJWT(
    loginData: Annotated[OAuth2PasswordRequestForm, Depends()],
    dbSession: DBSessionDep
) -> Token:
    user = validateUserCredentialsAndGetUser(dbSession, loginData.username, loginData.password)
    if not user:
        logger.warning(f"failed login attempt for user [{loginData.username}]")
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    accessToken = createAccessToken(data={"id": user.id})
    logger.info(f"The user [{loginData.username}] successfully logged in")
    return Token(access_token=accessToken, token_type="bearer")

@app.get(
    "/api/v1/users",
    summary="Retrieve all the available users",
    response_model=list[UserData],
    tags=["Admin endpoints"]
)
async def getUsers(dbSession: DBSessionDep, adminUser: AuthenticatedAdminDep):
    users = dbSession.scalars(
        select(User)
    ).all()
    logger.debug(f"the user {adminUser.username} accessed the admin endpoint [GET /api/v1/users]")
    return users

@app.post(
    "/api/v1/users",
    summary="Create a new user",
    response_model=UserData,
    tags=["Admin endpoints"]
)
async def createUser(userData: UserCreationData, dbSession: DBSessionDep, adminUser: AuthenticatedAdminDep):
    user = User(
        username=userData.username,
        password=userData.password,
        isAdmin=userData.is_admin
    )
    dbSession.add(user)
    dbSession.commit()
    dbSession.refresh(user)
    logger.info(f"the user [{adminUser.username}] created the user [{user.username}] with admin={user.is_admin}")
    return user


@app.get(
    "/api/v1/tags", 
    summary="Retrieve all the available DataType tags", 
    response_model=list[DataTypeTagResponse], 
    tags=["Admin endpoints"]
)
async def getDataTypeTags(session: DBSessionDep, adminUser: AuthenticatedAdminDep):
    tags = session.scalars(
        select(DataTypeTag)
    ).all()
    logger.debug(f"the user {adminUser.username} accessed the admin endpoint [GET /api/v1/tags]")

    return tags

@app.post(
    "/api/v1/tags", 
    summary="Create a new DataType tag",
    response_model=DataTypeTagResponse, 
    tags=["Admin endpoints"]
)
async def addDataTypeTag(data: DataTypeTagCreationData, session: DBSessionDep, adminUser: AuthenticatedAdminDep):
    newTag = DataTypeTag(name=data.name, description=data.description, createdBy=adminUser)
    session.add(newTag)
    session.commit()
    session.refresh(newTag)
    logger.info(f"the user [{adminUser.username}] created the new DataTypeTag [{newTag.name}]")

    return newTag


@app.get(
    "/api/v1/controls", 
    summary="Get all the available controls",
    response_model=list[ControlsResponse], 
    tags=["Admin endpoints"]
)
async def getControls(session: DBSessionDep, adminUser: AuthenticatedAdminDep):
    controls = session.scalars(
        select(Control)
    ).all()
    logger.debug(f"the user {adminUser.username} accessed the admin endpoint [GET /api/v1/controls]")

    return controls

@app.post(
    "/api/v1/controls/regexOnFieldName", 
    summary="Create a new control",
    response_model=ControlsResponse, 
    tags=["Admin endpoints"]
)
async def addControlRegExOnFieldName(data: RegExOnFieldNameControlCreationData, session: DBSessionDep, adminUser: AuthenticatedAdminDep):
    mappedTags = None
    try:
        mappedTags = data.parsedAffectedTags(session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    newControl = RegExOnFieldNameControl(
        name=data.name,
        affectedTags=mappedTags,
        regex=data.regex,
        createdBy=adminUser
    )
    session.add(newControl)
    session.commit()
    session.refresh(newControl)

    logger.info(f"the user [{adminUser.username}] created a new control of type RegExOnFieldName [{newControl.name}]")
    return newControl


@app.get(
    "/api/v1/databases", 
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


@app.post(
    "/api/v1/databases/mysql", 
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


@app.post(
    "/api/v1/databases/{id}/scans",
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
    
    scan = database.scanStructure(requestedBy=user)
    database.runControlsOnLastScan(controls)

    session.add(database)
    session.commit()

    logger.info(f"the user [{user.username}] requested a new scan for the database with id={database.id}")
    return scan


@app.get(
    "/api/v1/databases/{id}/scans",
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


@app.get(
    "/api/v1/databases/{id}/scans/last",
    summary="Get the results of the last scan on the database with id = {id}",
    tags=["Non-Admin endpoints"]
)
async def getDatabaseResults(id: int, session: DBSessionDep, user: AuthenticatedUserDep):
    database = session.scalars(
        select(ScanResult)
        .where(ScanResult.database_id == id)
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


@app.get(
    "/api/v1/databases/scans/{id}",
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