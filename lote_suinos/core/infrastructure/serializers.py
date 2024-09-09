from rest_framework import serializers
from lote_suinos.core.infrastructure.models import LoteModel
from lote_suinos.core.infrastructure.repository import LoteRedisRepositoryImpl


class LoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = LoteModel
        fields = ['uuid', 'status', 'lote_id', 'quantidade', 'created', 'updated']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        redis_data = LoteRedisRepositoryImpl().get_by_uuid(instance.uuid)
        if redis_data:
            representation['quantidade'] = redis_data
        return representation