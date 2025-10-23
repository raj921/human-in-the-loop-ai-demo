import asyncio
import uvicorn
import os
from pathlib import Path
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
import sqlite3
from datetime import datetime

from database import Database, RequestStatus
from customer_followup import CustomerFollowupService
from api_token import router as token_router

app = FastAPI(title="Glow Beauty Salon - Supervisor Dashboard")

# Enable CORS for frontend
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3005", "http://localhost:3006"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include token generation endpoint
app.include_router(token_router)

# Get the correct templates directory path
BASE_DIR = Path(__file__).parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

db = Database()
followup_service = CustomerFollowupService(db)

@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Main supervisor dashboard showing pending and resolved requests"""
    pending_requests = await db.get_pending_requests()
    all_requests = await db.get_all_requests()
    learned_answers = await db.get_learned_answers()
    
    # Check for timeout requests (older than 24 hours)
    await db.mark_timeout_requests(timeout_hours=24)
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "pending_requests": pending_requests,
        "all_requests": all_requests,
        "learned_answers": learned_answers,
        "pending_count": len(pending_requests)
    })

@app.post("/respond/{request_id}")
async def respond_to_request(request_id: str, response: str = Form(...)):
    """Handle supervisor response to a help request"""
    success = await db.resolve_help_request(request_id, response)
    
    if not success:
        raise HTTPException(status_code=404, detail="Request not found")
    
    # Get the request details for customer follow-up
    all_requests = await db.get_all_requests()
    target_request = None
    for req in all_requests:
        if req.id == request_id:
            target_request = req
            break
    
    # Send customer follow-up
    if target_request:
        await followup_service.send_customer_response(request_id)
    
    # Add to learned answers for future reference
    await db.add_learned_answer(target_request.question if target_request else "Unknown question", response)
    
    return RedirectResponse(url="/", status_code=303)

@app.post("/learned-answer")
async def add_learned_answer(question: str = Form(...), answer: str = Form(...)):
    """Manually add a learned answer"""
    await db.add_learned_answer(question, answer)
    return RedirectResponse(url="/", status_code=303)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
