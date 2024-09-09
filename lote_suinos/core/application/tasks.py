from celery import shared_task
from lote_suinos.core.application.lote import LoteService
from lote_suinos.core.infrastructure.repository import LoteRepositoryImpl, LoteRedisRepositoryImpl
import uuid

service = LoteService(LoteRepositoryImpl(), LoteRedisRepositoryImpl())

@shared_task
def create_lote_item_task(status: str, lote_id: str, quantidade: int):
    lote = service.create_lote_item(status=status, lote_id=lote_id, quantidade=quantidade)
    return lote.uuid

@shared_task
def update_lote_item_task(uuid: uuid.UUID, status: str, lote_id: str, quantidade: int):
    return service.update_lote(uuid=uuid, status=status, lote_id=lote_id, quantidade=quantidade)

@shared_task
def delete_lote_item_task(uuid: uuid.UUID):
    lote_item = service.get_lote_item(uuid)
    if lote_item:
        service.delete_lote_item(uuid)