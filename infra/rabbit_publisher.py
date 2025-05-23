import json
import aio_pika

from typing import Mapping, Any

from core.RabbitInterface import PublisherInterface


# TODO вынести в настройки, а там брать из .env!!!!
RABBITMQ_HOST = "185.100.67.246"
# RABBITMQ_HOST = "0.0.0.0"
RABBITMQ_PORT = 5672
RABBITMQ_USER = "guest"
RABBITMQ_PASSWORD = "guest"
QUEUE = "qr_events"


class AioPikaPublisher(PublisherInterface):
    queue = QUEUE

    def __init__(self) -> None:
        self._conn: aio_pika.RobustConnection | None = None
        self._channel: aio_pika.Channel | None = None

    # --- life‑cycle ---------------------------------------------------------
    async def connect(self) -> None:
        self._conn = await aio_pika.connect_robust(
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            login=RABBITMQ_USER,
            password=RABBITMQ_PASSWORD,
            heartbeat=30,
        )
        self._channel = await self._conn.channel()
        await self._channel.declare_queue(self.queue, durable=True)

    async def close(self) -> None:
        if self._conn and not self._conn.is_closed:
            await self._conn.close()

    # --- Publish API --------------------------------------------------------
    async def publish(
        self, message: Mapping[str, Any], queue: str | None = None
    ) -> None:
        if not self._channel:
            raise RuntimeError("Publisher not connected")

        target_queue = queue or self.queue

        if queue:
            await self._channel.declare_queue(target_queue, durable=True)

        await self._channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(message).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
            ),
            routing_key=target_queue,
        )
