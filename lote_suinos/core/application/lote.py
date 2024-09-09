from lote_suinos.core.domain.models import LoteItemRedis
from lote_suinos.core.domain.repositories import LoteRedisRepository
from lote_suinos.core.domain.models import LoteItem
from lote_suinos.core.domain.repositories import LoteRepository
import uuid
from datetime import datetime

class LoteService:
    def __init__(self, repository: LoteRepository, redis: LoteRedisRepository):
        self.repository = repository
        self.redis = redis

    def create_lote_item(self, status: str, lote_id: str, quantidade: int) -> LoteItem:
        lote_item = LoteItem(
            uuid=uuid.uuid4(),
            status=status,
            lote_id=lote_id,
            quantidade=quantidade,
            created=datetime.now(),
            updated=datetime.now()
        )

        lote_item_redis = LoteItemRedis(uuid = lote_item.uuid, quantidade = quantidade)
        self.redis.save(lote_item_redis)

        return self.repository.save(lote_item)

    def get_lote_item(self, uuid: uuid.UUID) -> LoteItem:
        return self.repository.get_by_uuid(uuid)

    def update_lote(self, uuid: uuid.UUID, status: str, lote_id: str, quantidade: int) -> LoteItem:
        lote_item = self.repository.get_by_uuid(uuid)
        if lote_item:
            lote_item.status = status
            lote_item.updated = datetime.now()
            lote_item.lote_id = lote_id
            lote_item.quantidade = quantidade

            lote_item_redis = LoteItemRedis(uuid=lote_item.uuid, quantidade=quantidade)
            self.redis.save(lote_item_redis)
            return self.repository.update(lote_item)
        return None

    def delete_lote_item(self, uuid: uuid.UUID):
        lote_item = self.repository.get_by_uuid(uuid)
        if lote_item:
            self.repository.delete(lote_item)
            self.redis.delete(uuid)