from django.db import models
from uuid import uuid4


class LoteModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    status = models.CharField(max_length=100, blank=True)
    lote_id = models.CharField(max_length=100, db_index=True)
    quantidade = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.lote_id