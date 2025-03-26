import sys
from loguru import logger
logger.remove()
logger.add("logs/DatabaseClasificationAPI_{time}.log",rotation="w6",format="{time:DD/MM/YYYY HH:mm:ss} - {level} - {message}")
logger.add(sys.stdout, colorize=True, format="<level>{time:DD/MM/YYYY HH:mm:ss} - {level} - {message}</level>")

from datetime import timedelta
from typing import Annotated
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from api.auth.JWTModels import Token
from api.auth.helperFunctions import createAccessToken, validateUserCredentialsAndGetUser

from api.databaseDependencies import DBSessionDep

from api.routers import controls, tags, users, databases

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

app.include_router(tags.router)
app.include_router(controls.router)
app.include_router(users.router)
app.include_router(databases.router)
