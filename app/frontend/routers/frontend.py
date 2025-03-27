from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="frontend/templates")

@router.get("/", response_class=HTMLResponse, tags=["GUI"])
async def root():
    return RedirectResponse(url="/databases")

@router.get("/login", response_class=HTMLResponse, tags=["GUI"])
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request, name="login.html"
    )

@router.get("/databases", response_class=HTMLResponse, tags=["GUI"])
async def read_item(request: Request):
    return templates.TemplateResponse(
        request=request, name="databases.html"
    )

@router.get("/results", response_class=HTMLResponse, tags=["GUI"])
async def read_item(request: Request, databaseId: int):
    return templates.TemplateResponse(
        request=request, name="results.html", context={"databaseId": databaseId}
    )
