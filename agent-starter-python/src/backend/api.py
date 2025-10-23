from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from .db import init_db, session_scope
from .models import RequestStatus
from .repositories import HelpRequestRepository, KnowledgeRepository
from .services import HelpdeskService, NotificationService


class CreateRequest(BaseModel):
    caller_id: str
    question: str


class RespondRequest(BaseModel):
    answer: str


app = FastAPI(title="Frontdesk Backend")


@app.on_event("startup")
def on_startup():
    init_db()


@app.post("/requests")
async def create_request(payload: CreateRequest):
    with session_scope() as session:
        help_repo = HelpRequestRepository(session)
        kb_repo = KnowledgeRepository(session)
        notifier = NotificationService()
        svc = HelpdeskService(help_repo, kb_repo, notifier)

        known_answer, req = svc.lookup_or_create_request(payload.caller_id, payload.question)
        if known_answer is not None:
            # Known answer: return immediately with answer and do not create DB row
            return {"known": True, "answer": known_answer}

        # Created a pending help request; notify supervisor
        await notifier.notify_supervisor(req)
        return {"known": False, "request_id": req.id, "status": req.status}


@app.get("/requests")
def list_requests(status: Optional[RequestStatus] = None):
    with session_scope() as session:
        help_repo = HelpRequestRepository(session)
        items = help_repo.list(status)
    return items


@app.post("/requests/{request_id}/respond")
async def respond_request(request_id: int, payload: RespondRequest):
    with session_scope() as session:
        help_repo = HelpRequestRepository(session)
        kb_repo = KnowledgeRepository(session)
        notifier = NotificationService()
        svc = HelpdeskService(help_repo, kb_repo, notifier)

        req = svc.resolve_request_and_learn(request_id, payload.answer)
        if not req:
            raise HTTPException(status_code=404, detail="Request not found")

        await notifier.notify_caller(req.caller_id, payload.answer, request_id)
        return req


@app.post("/timeouts/sweep")
def sweep_timeouts():
    with session_scope() as session:
        repo = HelpRequestRepository(session)
        count = repo.mark_timeouts()
        return {"unresolved": count}


@app.get("/knowledge")
def list_knowledge():
    with session_scope() as session:
        repo = KnowledgeRepository(session)
        return repo.list()


