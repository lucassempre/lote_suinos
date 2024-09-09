import uuid
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime

@dataclass
class LoteItem:
    uuid: uuid.UUID
    status: str
    lote_id: str
    quantidade: int
    created: Optional[datetime] = field(default=None)
    updated: Optional[datetime] = field(default=None)

@dataclass
class LoteItemRedis:
    uuid: uuid.UUID
    quantidade: int
