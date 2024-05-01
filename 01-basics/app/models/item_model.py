"""
Item Model
"""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, Field


class ItemInput(BaseModel):
    name: str = Field(min_length=1, default="Item 1")


class ItemModel(ItemInput):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    modified_at: Optional[datetime] = Field(default_factory=datetime.now)
