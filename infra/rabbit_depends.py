from fastapi import FastAPI, Request

from infra.rabbit_publisher import AioPikaPublisher
from core.RabbitInterface import PublisherInterface


def init_broker(app: FastAPI) -> None:
    """Создаём singleton‑инстанс и кладём в app.state."""
    app.state.publisher = AioPikaPublisher()


async def connect_broker(app: FastAPI) -> None:
    await app.state.publisher.connect()


async def disconnect_broker(app: FastAPI) -> None:
    await app.state.publisher.close()


# --- FastAPI dependency ----------------------------------------------------
# def get_publisher(app: FastAPI) -> PublisherInterface:
#     return app.state.publisher


async def publisher_dep(request: Request) -> PublisherInterface:
    return request.app.state.publisher
