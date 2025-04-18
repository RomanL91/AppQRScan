from fastapi import APIRouter

from api.callback_point import router_callback_point


router = APIRouter()

router.include_router(router=router_callback_point, prefix="/cb")
