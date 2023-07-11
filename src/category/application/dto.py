from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass(slots=True, frozen=True)
class CategoryOutput:
    id: str
    name: str
    description: Optional[str]
    is_active: bool
    created_at: datetime
    