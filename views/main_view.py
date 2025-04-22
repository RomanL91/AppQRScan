from fastapi import APIRouter, Request

from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


main_page_router = APIRouter(tags=["main"])
templates = Jinja2Templates("templates")


@main_page_router.get(
    "/",
    response_class=HTMLResponse,
    summary="Главная страница",
)
async def main_page(request: Request):
    return templates.TemplateResponse(
        "main.html",
        context={
            "request": request,
            "qr_api_base": "https://sck.kz/cb/api/qr/",  # TODO в настройки
        },
    )
