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
from livekit.plugins import noise_cancellation, silero, groq, elevenlabs
from livekit.plugins.turn_detector.multilingual import MultilingualModel

from database import Database
from question_classifier import QuestionClassifier

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

You should handle these types of questions independently WITHOUT escalating:
- Greetings: Respond warmly ("Hello! Welcome to Glow Beauty Salon!")
- Connection questions: ("Yes, I can hear you clearly!")
- Basic salon info: Hours, location, listed services, pricing
- Appointment questions: General booking information
- General inquiries: How to reach us, what to expect

For greetings, respond like: "Hello! Welcome to Glow Beauty Salon. How can I help you today?"
For connection checks, respond: "Yes, I can hear you perfectly!"
For basic salon questions, provide the information from your knowledge.

ONLY escalate to human supervisor for:
- Technical questions about treatments not in your service list
- Complex customer complaints or issues
- Questions requiring medical advice
- Pricing for services not mentioned above
- Staff availability or specialized appointment requests

Your responses should be professional, friendly, and concise. Greet customers warmly and help them efficiently.""",
        )
        self.db = Database()
        self.customer_phone = None

    @function_tool
    async def request_help(self, context: RunContext, question: str):
        """Request help from a human supervisor ONLY for complex questions beyond basic salon information.
        
        DO NOT use for: greetings, basic questions, pricing for listed services, hours, location.
        DO use for: specialized treatments, medical advice, complex complaints, staff availability.
        
        Args:
            question: The specific question that requires supervisor expertise
        """
        try:
            # First check if we've learned this before
            learned_answer = await self.check_learned_answers(context, question)
            if learned_answer:
                logger.info(f"Found learned answer for: {question}")
                return learned_answer
            
            logger.info(f"No learned answer found for: {question}")
            
            logger.info(f"Escalating to supervisor for: {question}")
            
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
            
            return "That's a great question! I don't have that information right now, but let me check with my supervisor to get you an accurate answer."
            
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

    # To add tools, use the @function_tool decorator.
    # Here's an example that adds a simple weather tool.
    # You also have to add `from livekit.agents import function_tool, RunContext` to the top of this file
    # @function_tool
    # async def lookup_weather(self, context: RunContext, location: str):
    #     """Use this tool to look up current weather information in the given location.
    #
    #     If the location is not supported by the weather service, the tool will indicate this. You must tell the user the location's weather is unavailable.
    #
    #     Args:
    #         location: The location to look up weather information for (e.g. city name)
    #     """
    #
    #     logger.info(f"Looking up weather for {location}")
    #
    #     return "sunny with a temperature of 70 degrees."


def prewarm(proc: JobProcess):
    # Prewarm VAD model for faster startup
    try:
        proc.userdata["vad"] = silero.VAD.load()
    except Exception as e:
        logger.warning(f"Failed to prewarm VAD: {e}")


async def entrypoint(ctx: JobContext):
    # Logging setup
    # Add any other context you want in all log entries here
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    # Set up a voice AI pipeline using Groq AI (for LLM and STT) and fallback TTS
    session = AgentSession(
        # Speech-to-text (STT) using Groq's Whisper integration
        stt=groq.STT(model="whisper-large-v3-turbo"),
        # Large Language Model (LLM) using Groq AI - Llama 4 Scout with 30K TPM
        llm=groq.LLM(model="meta-llama/llama-4-scout-17b-16e-instruct"),
        # Text-to-speech (TTS) using ElevenLabs (with working voice ID)
        tts=elevenlabs.TTS(voice_id="2EiwWnXFnvU5JabPnv8n"),  # Professional female voice
        # VAD for speech detection
        vad=ctx.proc.userdata["vad"],
        # Simple turn detection without multilingual model (avoids job context requirement)
        # You can enable this later if needed: turn_detection=MultilingualModel(),
        # allow the LLM to generate a response while waiting for the end of turn
        preemptive_generation=True,
    )

    # To use a realtime model instead of a voice pipeline, use the following session setup instead.
    # (Note: This is for the OpenAI Realtime API. For other providers, see https://docs.livekit.io/agents/models/realtime/))
    # 1. Install livekit-agents[openai]
    # 2. Set OPENAI_API_KEY in .env.local
    # 3. Add `from livekit.plugins import openai` to the top of this file
    # 4. Use the following session setup instead of the version above
    # session = AgentSession(
    #     llm=openai.realtime.RealtimeModel(voice="marin")
    # )

    # Metrics collection, to measure pipeline performance
    # For more information, see https://docs.livekit.io/agents/build/metrics/
    usage_collector = metrics.UsageCollector()

    @session.on("metrics_collected")
    def _on_metrics_collected(ev: MetricsCollectedEvent):
        metrics.log_metrics(ev.metrics)
        usage_collector.collect(ev.metrics)

    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Usage: {summary}")

    ctx.add_shutdown_callback(log_usage)

    # # Add a virtual avatar to the session, if desired
    # # For other providers, see https://docs.livekit.io/agents/models/avatar/
    # avatar = hedra.AvatarSession(
    #   avatar_id="...",  # See https://docs.livekit.io/agents/models/avatar/plugins/hedra
    # )
    # # Start the avatar and wait for it to join
    # await avatar.start(session, room=ctx.room)

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
