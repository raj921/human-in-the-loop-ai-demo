import asyncio
import logging
from datetime import datetime, timedelta
from database import Database  

logger = logging.getLogger("timeout_service")

class TimeoutService:
    def __init__(self, database: Database, timeout_hours: int = 24):
        self.db = database
        self.timeout_hours = timeout_hours
        self.running = False
    
    async def start_monitoring(self):
        """Start the timeout monitoring service"""
        self.running = True
        logger.info(f"Started timeout monitoring service (timeout: {self.timeout_hours} hours)")
        
        while self.running:
            try:
                await self.db.mark_timeout_requests(self.timeout_hours)
                await asyncio.sleep(300)  # Check every 5 minutes
            except Exception as e:
                logger.error(f"Error in timeout monitoring: {str(e)}")
                await asyncio.sleep(60)  # Wait 1 minute before retrying
    
    def stop_monitoring(self):
        """Stop the timeout monitoring service"""
        self.running = False
        logger.info("Stopped timeout monitoring service")
