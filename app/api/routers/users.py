

from fastapi import APIRouter
from loguru import logger
from sqlalchemy import select

from internal.models.User import User

from api.models.Users import UserCreationData, UserData

from api.auth.authorizationDependencies import AuthenticatedAdminDep
from api.databaseDependencies import DBSessionDep


router = APIRouter(prefix="/api/v1/users")

@router.get(
    "/",
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

@router.post(
    "/",
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