from typing import Optional

import httpx

from .repositories import HelpRequestRepository, KnowledgeRepository
from .config import settings
from .models import HelpRequest


class NotificationService:
    async def notify_supervisor(self, help_request: HelpRequest) -> None:
        message = f"Hey, I need help answering: {help_request.question} (request_id={help_request.id})"
        if settings.supervisor_webhook_url:
            try:
                async with httpx.AsyncClient(timeout=5) as client:
                    await client.post(settings.supervisor_webhook_url, json={
                        "type": "help_request",
                        "request_id": help_request.id,
                        "caller_id": help_request.caller_id,
                        "question": help_request.question,
                    })
            except Exception:
                if settings.notify_console_fallback:
                    print(f"[SUPERVISOR NOTIFY FAIL->CONSOLE] {message}")
        else:
            if settings.notify_console_fallback:
                print(f"[SUPERVISOR NOTIFY] {message}")

    async def notify_caller(self, caller_id: str, answer: str, request_id: int) -> None:
        # Simulated SMS/call-back; could post to a webhook for Twilio
        print(f"[CALLER {caller_id}] Follow-up for request {request_id}: {answer}")


class HelpdeskService:
    def __init__(self, help_repo: HelpRequestRepository, kb_repo: KnowledgeRepository, notifier: NotificationService):
        self.help_repo = help_repo
        self.kb_repo = kb_repo
        self.notifier = notifier

    def lookup_or_create_request(self, caller_id: str, question: str) -> tuple[Optional[str], HelpRequest]:
        kb = self.kb_repo.get_by_question(question)
        if kb:
            return kb.answer, HelpRequest(caller_id=caller_id, question=question)
        req = self.help_repo.create(caller_id=caller_id, question=question)
        return None, req

    def resolve_request_and_learn(self, request_id: int, answer: str) -> Optional[HelpRequest]:
        req = self.help_repo.resolve(request_id, answer)
        if not req:
            return None
        self.kb_repo.upsert_exact(req.question, answer)
        return req


