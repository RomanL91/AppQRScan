from enum import Enum
from fastapi import APIRouter, Query, Depends

from core.RabbitInterface import PublisherInterface
from infra.rabbit_depends import publisher_dep


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
    publisher: PublisherInterface = Depends(publisher_dep),
):
    """
    Простой эндпоинт‑приёмник данных из Web‑страницы/Telegram‑WebApp.
    """

    payload = {
        "operation": operation,
        "userId": userId,
        "qrData": qrData,
    }

    await publisher.publish(payload)

    return {"status": "queued", **payload}
