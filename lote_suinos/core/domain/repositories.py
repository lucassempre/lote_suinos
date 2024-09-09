from abc import ABC, abstractmethod
from lote_suinos.core.domain.models import LoteItem, LoteItemRedis
from typing import Optional, Union
import uuid

class LoteRepository(ABC):
    @abstractmethod
    def save(self, lote_item: LoteItem) -> LoteItem:
        pass

    @abstractmethod
    def update(self, lote_item: LoteItem) -> LoteItem:
        pass

    @abstractmethod
    def get_by_uuid(self, uuid: uuid.UUID) -> Optional[LoteItem]:
        pass

    @abstractmethod
    def delete(self, lote_item: LoteItem):
        pass

class LoteRedisRepository(ABC):
    @abstractmethod
    def save(self, lote_item_redis: LoteItemRedis) -> LoteItemRedis:
        pass

    @abstractmethod
    def update(self, lote_item_redis: LoteItemRedis) -> LoteItemRedis:
        pass

    @abstractmethod
    def get_by_uuid(self, uuid: uuid.UUID) -> Union[int, None]:
        pass

    @abstractmethod
    def delete(self, uuid: uuid.UUID) -> Optional[bool]:
        pass