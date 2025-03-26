from fastapi import APIRouter
from loguru import logger
from sqlalchemy import select

from api.models.DataTypeTag import DataTypeTagCreationData, DataTypeTagResponse
from api.auth.authorizationDependencies import AuthenticatedAdminDep
from api.databaseDependencies import DBSessionDep

from internal.models.DataTypeTag import DataTypeTag

router = APIRouter(prefix="/api/v1/tags")


@router.get(
    "/", 
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

@router.post(
    "/", 
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
