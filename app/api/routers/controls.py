from fastapi import APIRouter, HTTPException
from loguru import logger
from sqlalchemy import select

from api.models.Controls import ControlsResponse, RegExOnFieldNameControlCreationData
from api.auth.authorizationDependencies import AuthenticatedAdminDep
from api.databaseDependencies import DBSessionDep

from internal.models.Control import Control
from internal.models.RegExOnFieldNameControl import RegExOnFieldNameControl


router = APIRouter(prefix="/api/v1/controls")


@router.get(
    "/", 
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

@router.post(
    "/regexOnFieldName", 
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
