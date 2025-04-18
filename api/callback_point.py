from enum import Enum
from fastapi import APIRouter, Query


router_callback_point = APIRouter(tags=["callback"])


class Operation(str, Enum):
    load = "shipment"
    pack = "packing"


@router_callback_point.get(
    "/api/qr/",
    summary="Для обратного вызова от сканера QR",
)
async def receive_qr(
    operation: Operation = Query(..., description="ПОГРУЗКА или УПАКОВКА"),
    userId: int | None = Query(None, description="Telegram chat_id"),
    qrData: str = Query(..., description="Содержимое QR‑кода"),
):
    """
    Простой эндпоинт‑приёмник данных из Web‑страницы/Telegram‑WebApp.
    """

    # здесь можно добавить сохранение в БД, отправку ботом и т. д.
    return {
        "status": "ok",
        "operation": operation,
        "userId": userId,
        "qrData": qrData,
    }
