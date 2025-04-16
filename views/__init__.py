from fastapi import APIRouter

from views.main_view import main_page_router


router = APIRouter()

router.include_router(router=main_page_router, prefix="/m")
