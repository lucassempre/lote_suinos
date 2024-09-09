from django.test import TestCase
from django.utils import timezone
from lote_suinos.core.domain.models import LoteItem
from lote_suinos.core.infrastructure.repository import LoteRepositoryImpl, LoteRedisRepositoryImpl
from lote_suinos.core.application.lote import LoteService
import uuid


class LoteServiceTestCase(TestCase):

    def setUp(self):
        self.lote_repository = LoteRepositoryImpl()
        self.redis_repository = LoteRedisRepositoryImpl()
        self.service = LoteService(LoteRepositoryImpl(), LoteRedisRepositoryImpl())

        self.lote_item_uuid = uuid.uuid4()
        self.lote_item = LoteItem(
            uuid=self.lote_item_uuid,
            status="created",
            lote_id="lote_123",
            quantidade=10,
            created=timezone.now(),
            updated=timezone.now()
        )
        self.lote_repository.save(self.lote_item)

    def test_create_lote_item(self):
        new_lote_item = self.service.create_lote_item(
            status="created",
            lote_id="lote_333",
            quantidade=20
        )
        self.assertIsNotNone(new_lote_item)
        self.assertEqual(new_lote_item.status, "created")
        self.assertEqual(new_lote_item.lote_id, "lote_333")
        self.assertEqual(new_lote_item.quantidade, 20)

    def test_create_lote_item_redis(self):
        new_lote_item = self.service.create_lote_item(
            status="created",
            lote_id="lote_123",
            quantidade=30
        )

        lote_item_redis = self.redis_repository.get_by_uuid(new_lote_item.uuid)
        self.assertIsNotNone(lote_item_redis)
        self.assertEqual(lote_item_redis, 30)

    def test_get_lote_item(self):
        self.assertEqual(self.service.get_lote_item(self.lote_item_uuid).lote_id, self.lote_item.lote_id)

    def test_update_lote(self):
        self.service.update_lote(
            uuid=self.lote_item_uuid,
            status="atualizado",
            lote_id="lote_111",
            quantidade=30
        )
        updated_item = self.service.get_lote_item(self.lote_item_uuid)
        self.assertIsNotNone(updated_item)
        self.assertEqual(updated_item.status, "atualizado")
        self.assertEqual(updated_item.lote_id, "lote_111")
        self.assertEqual(updated_item.quantidade, 30)

        lote_item_redis = self.redis_repository.get_by_uuid(self.lote_item_uuid)
        self.assertIsNotNone(lote_item_redis)
        self.assertEqual(lote_item_redis, 30)

    def test_update_lote_redis(self):
        self.service.update_lote(
            uuid=self.lote_item_uuid,
            status="atualizando",
            lote_id="lote_333",
            quantidade=100
        )

        lote_item_redis = self.redis_repository.get_by_uuid(self.lote_item_uuid)
        self.assertIsNotNone(lote_item_redis)
        self.assertEqual(lote_item_redis, 100)

    def test_delete_lote_item(self):
        self.service.delete_lote_item(self.lote_item_uuid)
        self.assertIsNone(self.lote_repository.get_by_uuid(self.lote_item_uuid))

    def test_delete_lote_item_redis(self):
        self.service.delete_lote_item(self.lote_item_uuid)
        self.assertIsNone(self.redis_repository.get_by_uuid(self.lote_item_uuid))