from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from lote_suinos.core.infrastructure.models import LoteModel
from lote_suinos.core.infrastructure.repository import LoteRedisRepositoryImpl


class LoteIntegrationTests(APITestCase):
    def setUp(self):
        self.lote_data = {
            'status': 'created',
            'lote_id': '123_created',
            'quantidade': 100
        }
        self.update_data = {
            'status': 'velho',
            'lote_id': '1234',
            'quantidade': 200
        }
        self.novo_data = {
            'status': 'start',
            'lote_id': '1234_novo',
            'quantidade': 300
        }

        self.lote = LoteModel.objects.create(**self.lote_data)
        self.redis_repository = LoteRedisRepositoryImpl()

    def test_create_lote(self):
        response = self.client.post(reverse('lote-list'), self.novo_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        lote = LoteModel.objects.filter(lote_id='1234_novo')
        self.assertTrue(lote.exists())

        self.assertEqual(self.redis_repository.get_by_uuid(lote.first().uuid), 300)


    def test_read_lote(self):
        response = self.client.get(reverse('lote-detail', kwargs={'pk': self.lote.uuid}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['lote_id'], self.lote_data['lote_id'])

    def test_update_lote(self):
        response = self.client.put(reverse('lote-detail', kwargs={'pk': self.lote.uuid}), self.update_data,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LoteModel.objects.get(uuid=self.lote.uuid).lote_id, self.update_data['lote_id'])
        self.assertEqual(self.redis_repository.get_by_uuid(self.lote.uuid), 200)

    def test_delete_lote(self):
        response = self.client.delete(reverse('lote-detail', kwargs={'pk': self.lote.uuid}))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LoteModel.objects.count(), 0)

    def test_delete_lote_redis(self):
        response = self.client.put(reverse('lote-detail', kwargs={'pk': self.lote.uuid}), self.update_data,
                                   format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.delete(reverse('lote-detail', kwargs={'pk': self.lote.uuid}))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNone(self.redis_repository.get_by_uuid(self.lote.uuid))
