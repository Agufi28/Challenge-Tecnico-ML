import jwt
from jwt.exceptions import InvalidTokenError

from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select

from internal.models.User import User
from internal.secrets.Secrets import Secrets
from api.auth.JWTModels import TokenData
from api.databaseDependencies import DBSessionDep


OAuth2SchemeDep = OAuth2PasswordBearer(tokenUrl="api/v1/token")

async def getCurrentUser(token: Annotated[str, Depends(OAuth2SchemeDep)], dbSession: DBSessionDep):
    credentialsException = HTTPException(
        status_code=401,
        detail="The token is invalid or has expired.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, Secrets.getJwtSecret(), algorithms=[Secrets.getJwtAlgorithm()])
        userId = payload.get("id")
        if userId is None:
            raise credentialsException
        token_data = TokenData(id=userId)
    except InvalidTokenError:
        raise credentialsException
    
    user = dbSession.scalars(
        select(User)
        .where(User.id == token_data.id)
    ).first()

    if user is None:
        raise credentialsException
    return user

AuthenticatedUserDep = Annotated[User, Depends(getCurrentUser)]

async def getCurrentAdminUser(user: AuthenticatedUserDep):
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="You need administrator privilleges to access this site")
    return user

AuthenticatedAdminDep = Annotated[User, Depends(getCurrentAdminUser)]
