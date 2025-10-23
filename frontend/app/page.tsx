'use client'

import { useState } from 'react'
import dynamic from 'next/dynamic'
import SupervisorAccess from '@/components/SupervisorAccess'
import FeatureCard from '@/components/FeatureCard'
import { Badge } from '@/components/ui/badge'
import { Card } from '@/components/ui/card'
import { Phone, Users, Database } from 'lucide-react'
import LiveKitVoiceClient from '@/components/LiveKitVoiceClient'

// Dynamically import VoicePoweredOrb to avoid SSR issues
const VoicePoweredOrb = dynamic(
  () => import('@/components/ui/voice-powered-orb').then(mod => mod.VoicePoweredOrb),
  { ssr: false }
)

export default function Home() {
  const [voiceDetected, setVoiceDetected] = useState(false)
  const [isConnected, setIsConnected] = useState(false)
  
  return (
    <div className="min-h-screen bg-gradient-to-b from-slate-50 via-white to-slate-50">
      {/* Header */}
      <header className="bg-white/80 backdrop-blur-md border-b border-slate-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-5">
          <div className="flex justify-between items-center">
            <div className="flex items-center space-x-4">
              <div className="relative">
                <div className="w-12 h-12 bg-gradient-to-br from-blue-600 to-purple-600 rounded-xl flex items-center justify-center text-white font-bold shadow-lg shadow-blue-500/20">
                  GS
                </div>
                <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-white"></div>
              </div>
              <div>
                <h1 className="text-xl font-bold text-slate-900 tracking-tight">Glow Beauty Salon</h1>
                <p className="text-sm text-slate-600">AI Receptionist System</p>
              </div>
            </div>
            <Badge variant="outline" className="text-xs px-3 py-1 border-slate-300 text-slate-700">
              Demo Mode
            </Badge>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        {/* Hero Section */}
        <div className="text-center mb-20">
          <div className="max-w-4xl mx-auto">
            <div className="inline-flex items-center gap-2 bg-blue-50 border border-blue-200 text-blue-700 px-4 py-2 rounded-full text-sm font-medium mb-6">
              <div className="w-2 h-2 bg-blue-500 rounded-full animate-pulse"></div>
              Frontdesk Engineering Assessment
            </div>
            
            <h2 className="text-5xl font-bold text-slate-900 mb-6 tracking-tight leading-tight">
              Human-in-the-Loop
              <span className="block mt-2 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                AI Receptionist System
              </span>
            </h2>
            
            <p className="text-lg text-slate-600 leading-relaxed max-w-2xl mx-auto mb-8">
              Voice-enabled AI with intelligent escalation to human supervisors.
              Built with LiveKit, Groq AI, and ElevenLabs for real-time interactions.
            </p>
            
            <div className="flex flex-wrap justify-center gap-3">
              <div className="px-4 py-2 bg-white border border-slate-200 rounded-lg shadow-sm hover:shadow-md transition-shadow">
                <span className="text-sm font-medium text-slate-700">Voice Processing</span>
              </div>
              <div className="px-4 py-2 bg-white border border-slate-200 rounded-lg shadow-sm hover:shadow-md transition-shadow">
                <span className="text-sm font-medium text-slate-700">Smart Escalation</span>
              </div>
              <div className="px-4 py-2 bg-white border border-slate-200 rounded-lg shadow-sm hover:shadow-md transition-shadow">
                <span className="text-sm font-medium text-slate-700">Learning System</span>
              </div>
            </div>
          </div>
        </div>

        {/* Main Demo Section */}
        <div className="grid lg:grid-cols-2 gap-10 items-start mb-24">
          {/* Voice Interface */}
          <div className="lg:sticky top-24">
            <div className="mb-8">
              <div className="flex items-center gap-3 mb-3">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <Phone className="h-5 w-5 text-blue-600" />
                </div>
                <h3 className="text-2xl font-bold text-slate-900">Voice Interface</h3>
              </div>
              <p className="text-slate-600 leading-relaxed">
                Real-time voice conversation powered by LiveKit. Talk to the AI receptionist now!
              </p>
            </div>
            
            {/* Voice-Powered Orb */}
            <Card className="p-6 bg-black/5 border-slate-200 mb-6">
              <div className="w-full aspect-square relative mb-4">
                <VoicePoweredOrb
                  enableVoiceControl={isConnected}
                  className="rounded-xl overflow-hidden shadow-2xl"
                  onVoiceDetected={setVoiceDetected}
                  hue={isConnected ? 200 : 0}
                />
              </div>
              
              {/* Voice Indicator */}
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
            </Card>
            
            {/* Voice Controls */}
            <Card className="p-6">
              <LiveKitVoiceClient
                onVoiceDetected={setVoiceDetected}
                onConnectionChange={setIsConnected}
              />
            </Card>
            
            {/* Example Questions */}
            <Card className="p-4 bg-blue-50 border-blue-200 mt-4">
              <h4 className="font-semibold text-slate-900 mb-2 text-sm">Try asking:</h4>
              <ul className="space-y-1 text-xs text-slate-700">
                <li>• "What are your hours?"</li>
                <li>• "What services do you offer?"</li>
                <li>• "Do you offer microblading?" (AI escalates)</li>
              </ul>
            </Card>
          </div>

          {/* Supervisor Access */}
          <div>
            <div className="mb-8">
              <div className="flex items-center gap-3 mb-3">
                <div className="p-2 bg-purple-100 rounded-lg">
                  <Users className="h-5 w-5 text-purple-600" />
                </div>
                <h3 className="text-2xl font-bold text-slate-900">Supervisor Panel</h3>
              </div>
              <p className="text-slate-600 leading-relaxed">
                Human oversight dashboard for handling escalated requests and providing real-time guidance.
              </p>
            </div>
            <SupervisorAccess />
          </div>
        </div>

        {/* Feature Cards */}
        <div className="mb-24">
          <div className="text-center mb-12">
            <h3 className="text-3xl font-bold text-slate-900 mb-3">
              Key Features
            </h3>
            <p className="text-slate-600">
              Core capabilities of the system
            </p>
          </div>
          
          <div className="grid md:grid-cols-3 gap-8">
            <FeatureCard
              icon={<Phone />}
              title="Voice Processing"
              color="blue"
              description="Real-time speech recognition and synthesis using LiveKit"
            />
            
            <FeatureCard
              icon={<Users />}
              title="Human Escalation"
              color="green"
              description="Automatic escalation to human supervisors when needed"
            />
            
            <FeatureCard
              icon={<Database />}
              title="Learning System"
              color="purple"
              description="Stores supervisor responses for future reference"
            />
          </div>
        </div>

        {/* Technical Stack */}
        <div className="max-w-5xl mx-auto">
          <div className="text-center mb-12">
            <h3 className="text-3xl font-bold text-slate-900 mb-3">
              Technical Stack
            </h3>
            <p className="text-slate-600">
              Modern technologies powering the system
            </p>
          </div>
          
          <div className="grid md:grid-cols-2 gap-8">
            <div className="bg-white border border-slate-200 rounded-2xl p-8 shadow-sm hover:shadow-lg transition-shadow">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
                  <Database className="h-5 w-5 text-white" />
                </div>
                <h4 className="text-xl font-bold text-slate-900">Backend</h4>
              </div>
              <ul className="space-y-3">
                <li className="flex items-start gap-3">
                  <div className="w-1.5 h-1.5 bg-blue-500 rounded-full mt-2"></div>
                  <div>
                    <span className="font-semibold text-slate-900">LiveKit</span>
                    <p className="text-sm text-slate-600">Real-time voice processing</p>
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <div className="w-1.5 h-1.5 bg-blue-500 rounded-full mt-2"></div>
                  <div>
                    <span className="font-semibold text-slate-900">Groq AI</span>
                    <p className="text-sm text-slate-600">LLM inference engine</p>
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <div className="w-1.5 h-1.5 bg-blue-500 rounded-full mt-2"></div>
                  <div>
                    <span className="font-semibold text-slate-900">ElevenLabs</span>
                    <p className="text-sm text-slate-600">Text-to-speech synthesis</p>
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <div className="w-1.5 h-1.5 bg-blue-500 rounded-full mt-2"></div>
                  <div>
                    <span className="font-semibold text-slate-900">SQLite</span>
                    <p className="text-sm text-slate-600">Data persistence layer</p>
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <div className="w-1.5 h-1.5 bg-blue-500 rounded-full mt-2"></div>
                  <div>
                    <span className="font-semibold text-slate-900">FastAPI</span>
                    <p className="text-sm text-slate-600">REST API framework</p>
                  </div>
                </li>
              </ul>
            </div>
            
            <div className="bg-white border border-slate-200 rounded-2xl p-8 shadow-sm hover:shadow-lg transition-shadow">
              <div className="flex items-center gap-3 mb-6">
                <div className="w-10 h-10 bg-gradient-to-br from-purple-500 to-purple-600 rounded-lg flex items-center justify-center">
                  <Phone className="h-5 w-5 text-white" />
                </div>
                <h4 className="text-xl font-bold text-slate-900">Frontend</h4>
              </div>
              <ul className="space-y-3">
                <li className="flex items-start gap-3">
                  <div className="w-1.5 h-1.5 bg-purple-500 rounded-full mt-2"></div>
                  <div>
                    <span className="font-semibold text-slate-900">Next.js</span>
                    <p className="text-sm text-slate-600">React framework</p>
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <div className="w-1.5 h-1.5 bg-purple-500 rounded-full mt-2"></div>
                  <div>
                    <span className="font-semibold text-slate-900">TypeScript</span>
                    <p className="text-sm text-slate-600">Type-safe development</p>
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <div className="w-1.5 h-1.5 bg-purple-500 rounded-full mt-2"></div>
                  <div>
                    <span className="font-semibold text-slate-900">Tailwind CSS</span>
                    <p className="text-sm text-slate-600">Utility-first styling</p>
                  </div>
                </li>
                <li className="flex items-start gap-3">
                  <div className="w-1.5 h-1.5 bg-purple-500 rounded-full mt-2"></div>
                  <div>
                    <span className="font-semibold text-slate-900">shadcn/ui</span>
                    <p className="text-sm text-slate-600">Component library</p>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-slate-50 border-t border-slate-200 mt-32">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">
            <div className="inline-flex items-center gap-3 mb-4">
              <div className="w-10 h-10 bg-gradient-to-br from-blue-600 to-purple-600 rounded-xl flex items-center justify-center text-white font-bold shadow-lg shadow-blue-500/20">
                GS
              </div>
              <span className="text-lg font-bold text-slate-900">Glow Beauty Salon</span>
            </div>
            <p className="text-slate-600 text-sm mb-2">
              Frontdesk Engineering Assessment
            </p>
            <p className="text-slate-500 text-xs max-w-md mx-auto">
              Human-in-the-loop AI system with intelligent escalation and learning capabilities
            </p>
          </div>
        </div>
      </footer>
    </div>
  );


}
