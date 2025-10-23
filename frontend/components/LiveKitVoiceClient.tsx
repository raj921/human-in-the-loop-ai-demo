'use client'

import { useState, useEffect, useRef } from 'react'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Mic, MicOff, Phone, PhoneOff } from 'lucide-react'

interface LiveKitVoiceClientProps {
  onVoiceDetected?: (detected: boolean) => void
  onConnectionChange?: (connected: boolean) => void
}

export default function LiveKitVoiceClient({ 
  onVoiceDetected, 
  onConnectionChange 
}: LiveKitVoiceClientProps) {
  const [isConnected, setIsConnected] = useState(false)
  const [isConnecting, setIsConnecting] = useState(false)
  const [isMuted, setIsMuted] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [transcript, setTranscript] = useState<string[]>([])
  
  const roomRef = useRef<any>(null)
  const audioElementRef = useRef<HTMLAudioElement | null>(null)

  // LiveKit configuration
  const LIVEKIT_URL = 'wss://warm-transfer-demo-lisbwtug.livekit.cloud'

  const connectToAgent = async () => {
    setIsConnecting(true)
    setError(null)

    try {
      // Import LiveKit dynamically
      const { Room, RoomEvent, Track } = await import('livekit-client')
      
      // Generate token (simplified - in production, do server-side)
      const roomName = `salon-call-${Date.now()}`
      const token = await generateToken(roomName)

      // Create room
      const room = new Room({
        adaptiveStream: true,
        dynacast: true,
      })

      roomRef.current = room

      // Set up event listeners
      room.on(RoomEvent.Connected, () => {
        console.log('Connected to room')
        setIsConnected(true)
        setIsConnecting(false)
        onConnectionChange?.(true)
        addTranscript('System: Connected to AI receptionist')
      })

      room.on(RoomEvent.Disconnected, () => {
        console.log('Disconnected from room')
        setIsConnected(false)
        onConnectionChange?.(false)
        addTranscript('System: Disconnected')
      })

      room.on(RoomEvent.TrackSubscribed, (track, publication, participant) => {
        console.log('Track subscribed:', track.kind)
        
        if (track.kind === Track.Kind.Audio) {
          // Play remote audio (AI voice)
          const audioElement = track.attach()
          audioElement.play()
          audioElementRef.current = audioElement
          document.body.appendChild(audioElement)
        }
      })

      room.on(RoomEvent.TrackUnsubscribed, (track) => {
        track.detach()
      })

      room.on(RoomEvent.DataReceived, (payload) => {
        // Handle any data messages from agent
        const message = new TextDecoder().decode(payload)
        console.log('Received message:', message)
        addTranscript(`AI: ${message}`)
      })

      // Connect to room
      await room.connect(LIVEKIT_URL, token)

      // Enable microphone
      await room.localParticipant.setMicrophoneEnabled(true)
      
    } catch (err: any) {
      console.error('Failed to connect:', err)
      setError(err.message || 'Connection failed')
      setIsConnecting(false)
      addTranscript(`Error: ${err.message}`)
    }
  }

  const disconnect = () => {
    if (roomRef.current) {
      roomRef.current.disconnect()
      roomRef.current = null
    }
    
    if (audioElementRef.current) {
      audioElementRef.current.remove()
      audioElementRef.current = null
    }
    
    setIsConnected(false)
    onConnectionChange?.(false)
  }

  const toggleMute = async () => {
    if (roomRef.current && isConnected) {
      const newMutedState = !isMuted
      await roomRef.current.localParticipant.setMicrophoneEnabled(!newMutedState)
      setIsMuted(newMutedState)
      addTranscript(`System: Microphone ${newMutedState ? 'muted' : 'unmuted'}`)
    }
  }

  const addTranscript = (text: string) => {
    setTranscript(prev => [...prev.slice(-4), text]) // Keep last 5 messages
  }

  // Generate token (simplified - in production, this should be server-side)
  const generateToken = async (roomName: string): Promise<string> => {
    // For demo purposes, we'll use a simple fetch to a token endpoint
    // In your case, you might need to implement this server-side
    const response = await fetch(`http://localhost:8000/api/token?room=${roomName}`)
    if (!response.ok) {
      throw new Error('Failed to get token. Make sure backend is running.')
    }
    const data = await response.json()
    return data.token
  }

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      disconnect()
    }
  }, [])

  return (
    <div className="w-full space-y-4">
      {/* Connection Status */}
      <div className="text-center space-y-2">
        {isConnecting && (
          <p className="text-sm text-yellow-600">Connecting to AI receptionist...</p>
        )}
        {isConnected && (
          <p className="text-sm text-green-600 font-medium">✓ Connected - Start speaking!</p>
        )}
        {error && (
          <p className="text-sm text-red-600">Error: {error}</p>
        )}
      </div>

      {/* Control Buttons */}
      <div className="flex justify-center gap-4">
        {!isConnected ? (
          <Button
            onClick={connectToAgent}
            disabled={isConnecting}
            size="lg"
            className="px-8"
          >
            {isConnecting ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                Connecting...
              </>
            ) : (
              <>
                <Phone className="w-5 h-5 mr-2" />
                Call Receptionist
              </>
            )}
          </Button>
        ) : (
          <>
            <Button
              onClick={toggleMute}
              variant={isMuted ? "destructive" : "outline"}
              size="lg"
            >
              {isMuted ? (
                <>
                  <MicOff className="w-5 h-5 mr-2" />
                  Unmute
                </>
              ) : (
                <>
                  <Mic className="w-5 h-5 mr-2" />
                  Mute
                </>
              )}
            </Button>
            
            <Button
              onClick={disconnect}
              variant="destructive"
              size="lg"
            >
              <PhoneOff className="w-5 h-5 mr-2" />
              End Call
            </Button>
          </>
        )}
      </div>

      {/* Transcript */}
      {transcript.length > 0 && (
        <Card className="p-4 bg-slate-50">
          <h4 className="text-sm font-semibold mb-2">Conversation:</h4>
          <div className="space-y-1 text-sm">
            {transcript.map((line, i) => (
              <p key={i} className="text-slate-700">{line}</p>
            ))}
          </div>
        </Card>
      )}

      {/* Instructions */}
      <div className="text-center text-xs text-slate-500">
        <p>Click "Call Receptionist" to start a voice conversation</p>
        <p>The AI will answer your questions about Glow Beauty Salon</p>
      </div>
    </div>
  )
}
