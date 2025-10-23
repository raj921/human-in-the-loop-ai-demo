import logging
import uuid
import asyncio
from datetime import datetime

from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    MetricsCollectedEvent,
    RoomInputOptions,
    WorkerOptions,
    cli,
    metrics,
    function_tool,
    RunContext,
)
from livekit.plugins import noise_cancellation, silero, groq
from livekit.plugins.turn_detector.multilingual import MultilingualModel

from database import Database

logger = logging.getLogger("agent")

load_dotenv(".env.local")

class Assistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are a professional AI receptionist for "Glow Beauty Salon", a high-end beauty salon offering various services.

You know the following information about Glow Beauty Salon:
- Address: 123 Main Street, Downtown
- Phone: 555-0123
- Hours: Monday-Friday 9AM-7PM, Saturday 9AM-5PM, Closed Sunday
- Services: Haircuts, Hair Coloring, Styling, Manicures, Pedicures, Facials, Waxing
- Pricing: Haircuts $40-80, Hair Coloring $60-150, Manicures $25, Pedicures $45, Facials $60-120, Waxing $20-60
- Booking: Requires appointment, walk-ins occasionally available

If you don't know the answer to a specific question or need to provide information not covered above, you MUST escalate to a human supervisor.

Your responses should be professional, friendly, and concise. Greet customers warmly and help them efficiently.""",
        )
        self.db = Database()
        self.customer_phone = None

    @function_tool
    async def request_help(self, context: RunContext, question: str):
        """Request help from a human supervisor when you don't know the answer to a customer's question.
        
        Args:
            question: The specific question the customer asked that you cannot answer
        """
        try:
            logger.info(f"Requesting help for question: {question}")
            
            # Create help request
            request_id = str(uuid.uuid4())
            request = await self.db.create_help_request(
                id=request_id,
                customer_phone=self.customer_phone or "unknown",
                question=question
            )
            
            # Simulate supervisor notification (in real implementation, this would be a webhook/ SMS)
            message = f"🆘 SUPERVISOR ALERT: Need help answering customer question: '{question}' from {self.customer_phone or 'unknown customer'}. Request ID: {request_id}"
            print(f"\n{'='*50}")
            print(f"SUPERVISOR NOTIFICATION: {message}")
            print(f"{'='*50}\n")
            
            return "Let me check with my supervisor and get back to you with the answer to your question."
            
        except Exception as e:
            logger.error(f"Error requesting help: {str(e)}")
            return "I'm having trouble connecting with my supervisor right now. Please call us directly at 555-0123 for immediate assistance."

    @function_tool  
    async def check_learned_answers(self, context: RunContext, query: str):
        """Check if we have learned answers from previous supervisor responses.
        
        Args:
            query: The question or topic to search for in learned answers
        """
        try:
            answers = await self.db.search_learned_answers(query)
            
            if answers:
                best_match = answers[0]  # Take the most recent match
                return f"Based on previous learning: {best_match.answer}"
            
            return None
        except Exception as e:
            logger.error(f"Error checking learned answers: {str(e)}")
            return None

    def set_customer_phone(self, phone: str):
        """Set the customer's phone number for this session"""
        self.customer_phone = phone

def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()

async def entrypoint(ctx: JobContext):
    # Logging setup
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    # Set up a voice AI pipeline using Groq AI with simplified TTS
    session = AgentSession(
        # Speech-to-text (STT) using Groq's Whisper integration
        stt=groq.STT(model="whisper-large-v3-turbo"),
        # Large Language Model (LLM) using Groq AI
        llm=groq.LLM(model="llama-3.1-8b-instant"),
        # Text-to-speech using OpenAI's fallback (more reliable than ElevenLabs in some environments)
        tts="openai:tts-1-hd:alloy",
        # VAD for speech detection
        vad=ctx.proc.userdata["vad"],
        # Simple turn detection without multilingual model (avoids job context requirement)
        # You can enable this later if needed: turn_detection=MultilingualModel(),
        # allow the LLM to generate a response while waiting for the end of turn
        preemptive_generation=True,
    )

    # Metrics collection, to measure pipeline performance
    usage_collector = metrics.UsageCollector()

    @session.on("metrics_collected")
    def _on_metrics_collected(ev: MetricsCollectedEvent):
        metrics.log_metrics(ev.metrics)
        usage_collector.collect(ev.metrics)

    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Usage: {summary}")

    ctx.add_shutdown_callback(log_usage)

    # Start the session, which initializes the voice pipeline and warms up the models
    await session.start(
        agent=Assistant(),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            # For telephony applications, use `BVCTelephony` for best results
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    # Join the room and connect to the user
    await ctx.connect()

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))
