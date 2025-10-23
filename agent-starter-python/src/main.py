import asyncio
import logging
import threading
import subprocess
import sys
import time
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from database import Database
from timeout_service import TimeoutService
from customer_followup import CustomerFollowupService

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("main")

def run_web_server():
    """Run the FastAPI web server in a separate thread"""
    import uvicorn
    from web_server import app
    
    logger.info("Starting web server on http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")

def run_agent():
    """Run the LiveKit agent"""
    logger.info("Starting LiveKit agent in dev mode...")
    # Change to dev mode for continuous running
    subprocess.run([sys.executable, "src/agent.py", "dev"])

async def run_timeout_service():
    """Run the timeout monitoring service"""
    db = Database()
    timeout_service = TimeoutService(db, timeout_hours=24)
    await timeout_service.start_monitoring()

def main():
    """Main entry point that runs both web server and agent"""
    logger.info("🌟 Starting Glow Beauty Salon AI Receptionist System")
    
    # Initialize database
    db = Database()
    logger.info("Database initialized")
    
    # Start web server in a separate thread
    web_thread = threading.Thread(target=run_web_server, daemon=True)
    web_thread.start()
    
    # Give web server time to start
    time.sleep(2)
    
    print("\n" + "="*60)
    print("🌟 GLOW BEAUTY SALON - AI RECEPTIONIST SYSTEM")
    print("="*60)
    print("📊 Supervisor Dashboard: http://localhost:8000")
    print("🤖 AI Agent: Ready to receive calls via LiveKit")
    print("📱 Customer follow-up: Enabled")
    print("⏰ Timeout monitoring: Enabled (24 hours)")
    print("="*60)
    print("\n📋 Available commands:")
    print("1. Open http://localhost:8000 for supervisor dashboard")
    print("2. Use 'python src/agent.py console' to test agent locally")
    print("3. Use 'python src/agent.py dev' for development mode")
    print("4. Use Ctrl+C to stop the system")
    print("\n🎯 System is running... Press Ctrl+C to stop\n")
    
    try:
        # Run timeout service in background
        timeout_service_thread = threading.Thread(
            target=lambda: asyncio.run(run_timeout_service()),
            daemon=True
        )
        timeout_service_thread.start()
        
        # Keep the main thread running
        logger.info("✅ All services started. Press Ctrl+C to stop.")
        
        # Keep running until interrupted
        while True:
            time.sleep(1)
        
    except KeyboardInterrupt:
        logger.info("\n\n🛑 Shutting down system...")
        print("✅ Goodbye!")
    except Exception as e:
        logger.error(f"Error in main: {str(e)}")

if __name__ == "__main__":
    main()
