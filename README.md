# Human-in-the-Loop AI Receptionist

A comprehensive voice AI receptionist system that intelligently escalates to human supervisors when needed and learns from interactions over time.

## 🎯 Project Overview

This system demonstrates a complete human-in-the-loop AI supervisor workflow for a fictional beauty salon. The AI receptionist handles customer inquiries, escalates questions it can't answer to human supervisors, and automatically learns from supervisor responses to improve over time.

## ✨ Key Features

### 🤖 AI Agent Capabilities
- **Voice Assistant**: Full conversational AI using LiveKit with Groq AI and ElevenLabs
- **Business Knowledge**: Pre-trained with salon information (services, hours, pricing, location)
- **Smart Escalation**: Automatically requests human help when unable to answer
- **Learning**: Searches previous conversations for relevant answers

### 👥 Human Supervisor Tools
- **Web Dashboard**: Simple admin interface for monitoring and responding
- **Request Management**: View, prioritize, and resolve customer help requests
- **Knowledge Base**: Maintain learned answers for future use
- **Real-time Notifications**: Console-based alerts for new help requests

### 🔄 Automated Systems
- **Customer Follow-up**: Automatic SMS-style notifications with supervisor responses
- **Timeout Handling**: Marks unresolved requests as unresolved after 24 hours
- **Knowledge Integration**: Supervisor responses automatically added to knowledge base
- **Reliability**: Error handling and recovery throughout the system

## 🏗️ Architecture

### Core Components

1. **AI Receptionist (`src/agent.py`)**
   - LiveKit-based voice agent with Groq AI (LLM) and ElevenLabs (TTS/STT)
   - Salon business context with predefined knowledge
   - Function tools for help escalation and knowledge search

2. **Database Layer (`src/database.py`)**
   - SQLite database with three main tables:
     - `help_requests`: Customer questions and supervisor responses
     - `learned_answers`: Knowledge base of accumulated answers
   - Async database operations with proper error handling

3. **Supervisor Dashboard (`src/web_server.py`)**
   - FastAPI web application with Jinja2 templates
   - Real-time view of pending/resolved requests
   - Response interface and knowledge base management

4. **Customer Follow-up (`src/customer_followup.py`)**
   - Simulated SMS/webhook notifications to customers
   - Integration with supervisor response system
   - Logging and error handling

5. **Timeout Service (`src/timeout_service.py`)**
   - Background monitoring of unresolved requests
   - Automatic status updates after timeout period
   - Configurable timeout duration (default: 24 hours)

### Data Models

```
HelpRequest
├── id: string (UUID)
├── customer_phone: string
├── question: string
├── status: pending | resolved | unresolved
├── created_at: datetime
├── supervisor_response: string?
└── responded_at: datetime?

LearnedAnswer
├── id: string (UUID)
├── question: string
├── answer: string
└── learned_at: datetime
```

## 🚀 Setup Instructions

### Prerequisites
- Python 3.9+
- LiveKit Cloud account
- Groq AI API key
- ElevenLabs API key

### 1. Clone and Install Dependencies
```bash
cd agent-starter-python
uv sync
```

### 2. Environment Configuration
Create `.env.local` from `.env.example` and add your API keys:

```env
LIVEKIT_URL=wss://your-livekit-url.livekit.cloud
LIVEKIT_API_KEY=your-api-key
LIVEKIT_API_SECRET=your-api-secret

GROQ_API_KEY=your-groq-api-key
ELEVEN_API_KEY=your-elevenlabs-api-key
```

### 3. Download Required Models
```bash
uv run python src/agent.py download-files
```

### 4. Set Up LiveKit Cloud
1. Sign up at [LiveKit Cloud](https://cloud.livekit.io/)
2. Create a new application
3. Use the LiveKit CLI to authenticate:
```bash
lk cloud auth
lk app env -w -d .env.local
```

### 5. Run the System

#### Option A: Full System (Recommended)
```bash
uv run python src/main.py
```
This starts:
- Web dashboard at http://localhost:8000
- LiveKit agent ready for calls
- Timeout monitoring service
- Customer follow-up service

#### Option B: Individual Components
```bash
# Start just the web dashboard
uv run python src/agent.py dev

# Test agent in console
uv run python src/agent.py console
```

## 📋 Usage Guide

### For Customers
- Call the salon through LiveKit (requires frontend or SIP setup)
- AI receptionist answers with salon information
- If AI doesn't know the answer: "Let me check with my supervisor and get back to you"

### For Supervisors
1. Open http://localhost:8000
2. Monitor "Pending Help Requests" section
3. Respond to customer questions with detailed answers
4. View request history and learned answers
5. Manually add answers to knowledge base

### Testing the System

#### 1. Console Testing
```bash
uv run python src/agent.py console
```
Try questions like:
- "What are your hours?" (AI can answer)
- "Do you offer hair extensions?" (AI escalates for help)

#### 2. Web Interface Testing
1. Open the dashboard (localhost:8000)
2. Submit the form with "add learned answer" to test knowledge base
3. View the interface for pending requests and history

## 🔧 Technical Decisions

### Technology Stack
- **LiveKit Agents**: Real-time voice communication platform
- **Groq AI**: Fast LLM inference with clear pricing
- **ElevenLabs**: High-quality TTS and STT
- **FastAPI**: Simple, fast web framework for dashboard
- **SQLite**: Lightweight database suitable for demo scale
- **Jinja2**: Template engine for simple HTML interface



## 📄 License

MIT License - see LICENSE file for details.


