from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlmodel import SQLModel, Field


class RequestStatus(str, Enum):
    pending = "pending"
    resolved = "resolved"
    unresolved = "unresolved"


class HelpRequest(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    caller_id: str
    question: str
    status: RequestStatus = Field(default=RequestStatus.pending)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    resolved_at: Optional[datetime] = None
    answer: Optional[str] = None


class KnowledgeEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    question: str
    answer: str
    created_at: datetime = Field(default_factory=datetime.utcnow)


