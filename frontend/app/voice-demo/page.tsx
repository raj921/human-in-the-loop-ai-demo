'use client'

import { useState } from 'react'
import dynamic from 'next/dynamic'
import LiveKitVoiceClient from '@/components/LiveKitVoiceClient'
import { Card } from '@/components/ui/card'

// Dynamically import VoicePoweredOrb to avoid SSR issues
const VoicePoweredOrb = dynamic(
  () => import('@/components/ui/voice-powered-orb').then(mod => mod.VoicePoweredOrb),
  { ssr: false }
)

export default function VoiceDemoPage() {
  const [voiceDetected, setVoiceDetected] = useState(false)
  const [isConnected, setIsConnected] = useState(false)

  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 via-white to-slate-50 py-16 px-4">
      <div className="max-w-4xl mx-auto space-y-8">
        {/* Header */}
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-bold text-slate-900">
            Voice-Powered AI Receptionist
          </h1>
          <p className="text-slate-600">
            Talk to Glow Beauty Salon's AI assistant with real-time voice interaction
          </p>
        </div>

        {/* Main Demo Area */}
        <div className="grid md:grid-cols-2 gap-8 items-center">
          {/* Left: Visual Orb */}
          <div className="space-y-4">
            <Card className="p-8 bg-black/5 border-slate-200">
              <div className="w-full aspect-square relative">
                <VoicePoweredOrb
                  enableVoiceControl={isConnected}
                  className="rounded-xl overflow-hidden shadow-2xl"
                  onVoiceDetected={setVoiceDetected}
                  hue={isConnected ? 200 : 0}
                />
              </div>
              
              {/* Voice Indicator */}
              <div className="text-center mt-4">
                {isConnected && (
                  <div className="flex items-center justify-center gap-2">
                    <div className={`w-3 h-3 rounded-full ${
                      voiceDetected ? 'bg-green-500 animate-pulse' : 'bg-slate-300'
                    }`}></div>
                    <span className="text-sm text-slate-600">
                      {voiceDetected ? 'Voice Detected' : 'Listening...'}
                    </span>
                  </div>
                )}
              </div>
            </Card>

            <div className="text-sm text-slate-600 space-y-1">
              <p>✨ The orb responds to your voice in real-time</p>
              <p>🎤 Speak louder to see stronger effects</p>
              <p>🌊 Watch it animate as you talk</p>
            </div>
          </div>

          {/* Right: Voice Controls */}
          <div className="space-y-6">
            <Card className="p-8">
              <h2 className="text-2xl font-bold text-slate-900 mb-6">
                Start Conversation
              </h2>
              
              <LiveKitVoiceClient
                onVoiceDetected={setVoiceDetected}
                onConnectionChange={setIsConnected}
              />
            </Card>

            {/* Example Questions */}
            <Card className="p-6 bg-slate-50 border-slate-200">
              <h3 className="font-semibold text-slate-900 mb-3">
                Try asking:
              </h3>
              <ul className="space-y-2 text-sm text-slate-700">
                <li>• "What are your hours?"</li>
                <li>• "What services do you offer?"</li>
                <li>• "How much is a haircut?"</li>
                <li>• "Do you offer microblading?" (AI will escalate)</li>
                <li>• "Where are you located?"</li>
              </ul>
            </Card>
          </div>
        </div>

        {/* How It Works */}
        <Card className="p-8 bg-gradient-to-r from-blue-50 to-purple-50 border-slate-200">
          <h3 className="text-xl font-bold text-slate-900 mb-4">
            How It Works
          </h3>
          <div className="grid md:grid-cols-3 gap-6 text-sm">
            <div>
              <div className="font-semibold text-slate-900 mb-2">1. Voice Recognition</div>
              <p className="text-slate-600">
                LiveKit captures your voice in real-time and sends it to the AI agent
              </p>
            </div>
            <div>
              <div className="font-semibold text-slate-900 mb-2">2. AI Processing</div>
              <p className="text-slate-600">
                Groq AI processes your question and generates a natural response
              </p>
            </div>
            <div>
              <div className="font-semibold text-slate-900 mb-2">3. Voice Response</div>
              <p className="text-slate-600">
                ElevenLabs converts AI text to natural speech that you hear
              </p>
            </div>
          </div>
        </Card>

        {/* System Status */}
        <div className="text-center text-sm text-slate-500">
          <p>Make sure your backend is running on port 8000</p>
          <p>Agent should be running with: <code className="bg-slate-200 px-2 py-1 rounded">uv run python src/agent.py dev</code></p>
        </div>
      </div>
    </div>
  )
}
