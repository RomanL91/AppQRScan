from enum import Enum
from fastapi import (
    Request,
    APIRouter,
    HTTPException,
    Query,
    Depends,
)
from pydantic import BaseModel

from core.RabbitInterface import PublisherInterface
from infra.rabbit_depends import publisher_dep


router_callback_point = APIRouter(tags=["callback"])


class Operation(str, Enum):
    load = "shipment"
    pack = "packing"
    work = "work"


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


# MOCK_DATA_EXAMPLE = {
#     "id": 123123,
#     "m": 4,
#     "v": 15,
#     "city_from": "Астана",
#     "city_to": "Караганда",
# }


class QRScanPayload(BaseModel):
    operation: str  # только для "work"
    userId: int
    qrData: dict


@router_callback_point.post("/api/cargo_qr/")
async def handle_qr_scan(
    request: Request,
    publisher: PublisherInterface = Depends(publisher_dep),
):
    body = await request.json()

    payload = QRScanPayload(**body)

    if payload.operation != "work":
        raise HTTPException(status_code=400, detail="Операция не поддерживается")

    await publisher.publish(payload.model_dump(), queue="work_qr_queue")

    return {"status": "queued", **payload.model_dump()}
