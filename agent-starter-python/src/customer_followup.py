import asyncio
import logging
from datetime import datetime
from typing import Dict, Optional
from database import Database, HelpRequest

logger = logging.getLogger("customer_followup")

class CustomerFollowupService:
    def __init__(self, database: Database):
        self.db = database
    
    async def send_customer_response(self, request_id: str) -> bool:
        """Send the supervisor's response back to the customer"""
        try:
            # Get the updated request with supervisor response
            all_requests = await self.db.get_all_requests()
            target_request = None
            
            for request in all_requests:
                if request.id == request_id and request.status.value == "resolved":
                    target_request = request
                    break
            
            if not target_request or not target_request.supervisor_response:
                logger.error(f"No valid resolved request found for ID: {request_id}")
                return False
            
            # Simulate sending SMS/webhook to customer
            success = await self._simulate_customer_notification(
                phone=target_request.customer_phone,
                message=target_request.supervisor_response,
                question=target_request.question
            )
            
            if success:
                logger.info(f"Successfully sent follow-up to customer {target_request.customer_phone}")
                return True
            else:
                logger.error(f"Failed to send follow-up to customer {target_request.customer_phone}")
                return False
                
        except Exception as e:
            logger.error(f"Error in customer follow-up for request {request_id}: {str(e)}")
            return False
    
    async def _simulate_customer_notification(self, phone: str, message: str, question: str) -> bool:
        """Simulate sending an SMS/webhook to the customer"""
        try:
            # In a real implementation, this would integrate with:
            # - Twilio SMS API
            # - Custom webhook
            # - Push notification service
            
            notification = f"""
🌟 GLOW BEAUTY SALON - RESPONSE TO YOUR QUESTION

Original Question: "{question}"

Our Response: {message}

Thank you for contacting Glow Beauty Salon! 
To book an appointment, call us at 555-0123.

---
Message sent to: {phone}
Sent at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
            
            print(f"\n{'='*60}")
            print("📱 CUSTOMER FOLLOW-UP MESSAGE")
            print(f"{'='*60}")
            print(notification)
            print(f"{'='*60}\n")
            
            # Simulate network delay
            await asyncio.sleep(0.5)
            
            return True
            
        except Exception as e:
            logger.error(f"Error simulating customer notification: {str(e)}")
            return False
    
    async def check_and_send_followups(self):
        """Check for resolved requests that haven't been followed up with"""
        try:
            all_requests = await self.db.get_all_requests()
            
            for request in all_requests:
                if request.status.value == "resolved" and request.responded_at:
                    # Check if we should send follow-up (newly resolved)
                    time_since_response = datetime.now() - request.responded_at
                    
                    # Send follow-up for recently resolved requests
                    if time_since_response.total_seconds() < 60:  # Within last minute
                        await self.send_customer_response(request.id)
                        
        except Exception as e:
            logger.error(f"Error in check_and_send_followups: {str(e)}")
