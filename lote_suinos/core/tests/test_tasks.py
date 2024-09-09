from django.test import TestCase
from lote_suinos.core.application.lote import LoteService
from lote_suinos.core.infrastructure.repository import LoteRepositoryImpl, LoteRedisRepositoryImpl
from lote_suinos.core.application.tasks import create_lote_item_task, update_lote_item_task, delete_lote_item_task
import uuid


class CeleryTasksTests(TestCase):
    def setUp(self):
        self.lote_service = LoteService(LoteRepositoryImpl(), LoteRedisRepositoryImpl())
        self.lote = self.lote_service.create_lote_item(
            status='created',
            lote_id='teste_123',
            quantidade=100
        )

    def test_create_lote_item_task(self):
        result = create_lote_item_task.apply_async(('created', 'teste_created_123', 200))
        self.assertTrue(result.successful())
        self.assertIsInstance(result.result, uuid.UUID)
        self.assertEqual(
            self.lote_service.get_lote_item(result.result).quantidade,
            200
        )

    def test_update_lote_item_task(self):
        result = update_lote_item_task.apply_async((self.lote.uuid, 'updated', 'teste_update123', 300))
        self.assertTrue(result.successful())
        lote_item = self.lote_service.get_lote_item(self.lote.uuid)
        self.assertEqual(lote_item.status, 'updated')
        self.assertEqual(lote_item.quantidade, 300)

    def test_delete_lote_item_task(self):
        result = delete_lote_item_task.apply_async((self.lote.uuid,))
        self.assertTrue(result.successful())
        self.assertIsNone(self.lote_service.get_lote_item(self.lote.uuid))