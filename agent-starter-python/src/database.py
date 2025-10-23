import sqlite3
import asyncio
from datetime import datetime, timedelta
from typing import Optional, List
from dataclasses import dataclass
from enum import Enum

class RequestStatus(Enum):
    PENDING = "pending"
    RESOLVED = "resolved"
    UNRESOLVED = "unresolved"

@dataclass
class HelpRequest:
    id: str
    customer_phone: str
    question: str
    status: RequestStatus
    created_at: datetime
    supervisor_response: Optional[str] = None
    responded_at: Optional[datetime] = None

@dataclass
class LearnedAnswer:
    id: str
    question: str
    answer: str
    learned_at: datetime

class Database:
    def __init__(self, db_path: str = "help_requests.db"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create help_requests table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS help_requests (
                id TEXT PRIMARY KEY,
                customer_phone TEXT NOT NULL,
                question TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL,
                supervisor_response TEXT,
                responded_at TIMESTAMP
            )
        ''')
        
        # Create learned_answers table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS learned_answers (
                id TEXT PRIMARY KEY,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                learned_at TIMESTAMP NOT NULL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    async def create_help_request(self, id: str, customer_phone: str, question: str) -> HelpRequest:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        request = HelpRequest(
            id=id,
            customer_phone=customer_phone,
            question=question,
            status=RequestStatus.PENDING,
            created_at=datetime.now()
        )
        
        cursor.execute('''
            INSERT INTO help_requests (id, customer_phone, question, status, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (request.id, request.customer_phone, request.question, request.status.value, request.created_at))
        
        conn.commit()
        conn.close()
        return request
    
    async def get_pending_requests(self) -> List[HelpRequest]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, customer_phone, question, status, created_at, supervisor_response, responded_at
            FROM help_requests
            WHERE status = 'pending'
            ORDER BY created_at
        ''')
        
        requests = []
        for row in cursor.fetchall():
            requests.append(HelpRequest(
                id=row[0],
                customer_phone=row[1],
                question=row[2],
                status=RequestStatus(row[3]),
                created_at=datetime.fromisoformat(row[4]),
                supervisor_response=row[5],
                responded_at=datetime.fromisoformat(row[6]) if row[6] else None
            ))
        
        conn.close()
        return requests
    
    async def resolve_help_request(self, id: str, response: str) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE help_requests
            SET status = 'resolved', supervisor_response = ?, responded_at = ?
            WHERE id = ?
        ''', (response, datetime.now(), id))
        
        result = cursor.rowcount > 0
        conn.commit()
        conn.close()
        return result
    
    async def get_all_requests(self) -> List[HelpRequest]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, customer_phone, question, status, created_at, supervisor_response, responded_at
            FROM help_requests
            ORDER BY created_at DESC
        ''')
        
        requests = []
        for row in cursor.fetchall():
            requests.append(HelpRequest(
                id=row[0],
                customer_phone=row[1],
                question=row[2],
                status=RequestStatus(row[3]),
                created_at=datetime.fromisoformat(row[4]),
                supervisor_response=row[5],
                responded_at=datetime.fromisoformat(row[6]) if row[6] else None
            ))
        
        conn.close()
        return requests
    
    async def mark_timeout_requests(self, timeout_hours: int = 24):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timeout_time = datetime.now() - timedelta(hours=timeout_hours)
        
        cursor.execute('''
            UPDATE help_requests
            SET status = 'unresolved'
            WHERE status = 'pending' AND created_at < ?
        ''', (timeout_time,))
        
        conn.commit()
        conn.close()
    
    async def add_learned_answer(self, question: str, answer: str) -> LearnedAnswer:
        import uuid
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        learned = LearnedAnswer(
            id=str(uuid.uuid4()),
            question=question,
            answer=answer,
            learned_at=datetime.now()
        )
        
        cursor.execute('''
            INSERT INTO learned_answers (id, question, answer, learned_at)
            VALUES (?, ?, ?, ?)
        ''', (learned.id, learned.question, learned.answer, learned.learned_at))
        
        conn.commit()
        conn.close()
        return learned
    
    async def get_learned_answers(self) -> List[LearnedAnswer]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, question, answer, learned_at
            FROM learned_answers
            ORDER BY learned_at DESC
        ''')
        
        answers = []
        for row in cursor.fetchall():
            answers.append(LearnedAnswer(
                id=row[0],
                question=row[1],
                answer=row[2],
                learned_at=datetime.fromisoformat(row[3])
            ))
        
        conn.close()
        return answers
    
    async def search_learned_answers(self, query: str) -> List[LearnedAnswer]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, question, answer, learned_at
            FROM learned_answers
            WHERE question LIKE ? OR answer LIKE ?
            ORDER BY learned_at DESC
        ''', (f'%{query}%', f'%{query}%'))
        
        answers = []
        for row in cursor.fetchall():
            answers.append(LearnedAnswer(
                id=row[0],
                question=row[1],
                answer=row[2],
                learned_at=datetime.fromisoformat(row[3])
            ))
        
        conn.close()
        return answers
