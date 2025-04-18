from abc import ABC, abstractmethod
from typing import Mapping, Any


class PublisherInterface(ABC):
    """Абстракция для отправки сообщений во внешнюю шину."""

    @abstractmethod
    async def publish(self, message: Mapping[str, Any]) -> None: ...
