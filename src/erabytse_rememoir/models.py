from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

class MemoryEpisode(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid7()))
    user_id: str
    agent_id: str = "default_agent"
    content: str
    content_type: str = "note"  # conversation, feedback, observation, etc.
    embedding: List[float] = Field(default_factory=list)
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat())
    source: str = "user"  # "user" or "agent"
    context_tags: List[str] = Field(default_factory=list)
    confidence: float = 1.0
    version: int = 1
    parent_id: Optional[str] = None
    is_active: bool = True