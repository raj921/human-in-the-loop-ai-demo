from datetime import datetime, timedelta
from typing import Optional, Sequence

from sqlmodel import Session, select

from .config import settings
from .models import HelpRequest, KnowledgeEntry, RequestStatus


class HelpRequestRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, caller_id: str, question: str) -> HelpRequest:
        help_req = HelpRequest(caller_id=caller_id, question=question)
        self.session.add(help_req)
        self.session.flush()
        return help_req

    def get(self, request_id: int) -> Optional[HelpRequest]:
        return self.session.get(HelpRequest, request_id)

    def list(self, status: Optional[RequestStatus] = None) -> Sequence[HelpRequest]:
        stmt = select(HelpRequest)
        if status:
            stmt = stmt.where(HelpRequest.status == status)
        stmt = stmt.order_by(HelpRequest.created_at.desc())
        return list(self.session.exec(stmt))

    def resolve(self, request_id: int, answer: str) -> Optional[HelpRequest]:
        req = self.get(request_id)
        if not req:
            return None
        req.answer = answer
        req.status = RequestStatus.resolved
        req.resolved_at = datetime.utcnow()
        req.updated_at = datetime.utcnow()
        self.session.add(req)
        self.session.flush()
        return req

    def mark_timeouts(self) -> int:
        cutoff = datetime.utcnow() - timedelta(seconds=settings.request_timeout_seconds)
        stmt = select(HelpRequest).where(
            HelpRequest.status == RequestStatus.pending,
            HelpRequest.created_at < cutoff,
        )
        items = list(self.session.exec(stmt))
        for req in items:
            req.status = RequestStatus.unresolved
            req.updated_at = datetime.utcnow()
            self.session.add(req)
        self.session.flush()
        return len(items)


class KnowledgeRepository:
    def __init__(self, session: Session):
        self.session = session

    def upsert_exact(self, question: str, answer: str) -> KnowledgeEntry:
        existing = self.get_by_question(question)
        if existing:
            existing.answer = answer
            self.session.add(existing)
            self.session.flush()
            return existing
        entry = KnowledgeEntry(question=question, answer=answer)
        self.session.add(entry)
        self.session.flush()
        return entry

    def get_by_question(self, question: str) -> Optional[KnowledgeEntry]:
        stmt = select(KnowledgeEntry).where(KnowledgeEntry.question == question)
        return self.session.exec(stmt).first()

    def list(self) -> Sequence[KnowledgeEntry]:
        stmt = select(KnowledgeEntry).order_by(KnowledgeEntry.created_at.desc())
        return list(self.session.exec(stmt))


