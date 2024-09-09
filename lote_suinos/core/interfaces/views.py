from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from lote_suinos.core.infrastructure.serializers import LoteSerializer
from lote_suinos.core.infrastructure.models import LoteModel
from lote_suinos.core.application.tasks import create_lote_item_task, update_lote_item_task, delete_lote_item_task
import uuid
from drf_yasg.utils import swagger_auto_schema


class LoteViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = LoteModel.objects.all()
        serializer = LoteSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=LoteSerializer)
    def create(self, request):
        serializer = LoteSerializer(data=request.data)
        if serializer.is_valid():
            create_lote_item_task.delay(
                serializer.validated_data['status'],
                serializer.validated_data['lote_id'],
                serializer.validated_data['quantidade']
            )
            return Response({'message': 'Tarefa de inserção de lote criada'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        lote_item = LoteModel.objects.get(uuid=pk)
        serializer = LoteSerializer(lote_item)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=LoteSerializer)
    def update(self, request, pk=None):
        lote_item = LoteModel.objects.get(uuid=pk)
        serializer = LoteSerializer(lote_item, data=request.data)
        if serializer.is_valid():
            update_lote_item_task.delay(
                uuid=uuid.UUID(pk),
                status=serializer.validated_data['status'],
                lote_id=serializer.validated_data['lote_id'],
                quantidade=serializer.validated_data['quantidade']
            )
            return Response({'message': 'Tarefa de autialização de lote criada'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            delete_lote_item_task.delay(uuid=uuid.UUID(pk))
            return Response({'message': 'Tarefa de remoção de lote criada'}, status=status.HTTP_201_CREATED)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)