
from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
from sqlalchemy import select
from sqlalchemy.orm import Session

from internal.models.User import User
from internal.secrets.Secrets import Secrets


def validateUserCredentialsAndGetUser(dbSession: Session, username: str, password: str):
    user = dbSession.scalars(
        select(User)
        .where(User.username == username)
    ).first()

    # If the user exists and the password matches the hash, return the user. Otherwise return None.
    if user is not None and bcrypt.checkpw(password.encode(), user._password_hash.encode()):
        user.last_login = datetime.now()
        dbSession.add(user) # We save the updated last_login timestamp
        dbSession.commit()
        return user
    else:
        return None

def createAccessToken(data: dict):
    dataToEncode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=Secrets.getJwtDurationMinutes())
    dataToEncode.update({"exp": expire})
    encodedJWT = jwt.encode(dataToEncode, Secrets.getJwtSecret(), algorithm=Secrets.getJwtAlgorithm())

    return encodedJWT
