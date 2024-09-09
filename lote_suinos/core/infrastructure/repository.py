from lote_suinos.core.domain.models import LoteItem, LoteItemRedis
from lote_suinos.core.domain.repositories import LoteRepository, LoteRedisRepository
from lote_suinos.core.infrastructure.models import LoteModel
from django_redis import get_redis_connection
from typing import Optional, Union
import uuid, json

class LoteRepositoryImpl(LoteRepository):
    def save(self, lote_item: LoteItem) -> LoteItem:
        model_instance = LoteModel(
            uuid=lote_item.uuid,
            status=lote_item.status,
            lote_id=lote_item.lote_id,
            quantidade=lote_item.quantidade,
            created=lote_item.created,
            updated=lote_item.updated
        )
        model_instance.save()
        return lote_item

    def update(self, lote_item: LoteItem) -> LoteItem:
        return LoteModel.objects.filter(uuid=lote_item.uuid).update(
            status=lote_item.status,
            lote_id=lote_item.lote_id,
            quantidade=lote_item.quantidade
        )


    def get_by_uuid(self, uuid: uuid.UUID) -> Optional[LoteItem]:
        try:
            model_instance = LoteModel.objects.get(uuid=uuid)
            return LoteItem(
                uuid=model_instance.uuid,
                status=model_instance.status,
                lote_id=model_instance.lote_id,
                quantidade=model_instance.quantidade,
                created=model_instance.created,
                updated=model_instance.updated
            )
        except LoteModel.DoesNotExist:
            return None

    def delete(self, lote_item: LoteItem):
        LoteModel.objects.filter(uuid=lote_item.uuid).delete()

class LoteRedisRepositoryImpl(LoteRedisRepository):

    def __init__(self):
        self.redis = get_redis_connection("default")

    def save(self, lote_item: LoteItemRedis) -> LoteItemRedis:
        self.redis.set(f"lote_item:{lote_item.uuid}", lote_item.quantidade)
        return lote_item

    def update(self, lote_item: LoteItemRedis) -> LoteItemRedis:
        return self.save(lote_item)

    def get_by_uuid(self, uuid: uuid.UUID) -> Union[int, None]:
        data = self.redis.get(f"lote_item:{uuid}")
        if data is None:
            return None
        return json.loads(data)


    def delete(self, uuid: uuid.UUID) -> Optional[bool]:
       return self.redis.delete(f"lote_item:{uuid}")