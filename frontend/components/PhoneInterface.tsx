'use client'

import { useState } from 'react'
import { Phone, PhoneOff, Mic, MicOff, CheckCircle, AlertCircle } from 'lucide-react'
import { Card } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Progress } from '@/components/ui/progress'
import { Skeleton } from '@/components/ui/skeleton'
import { Alert, AlertTitle, AlertDescription } from '@/components/ui/alert'

export default function PhoneInterface() {
  const [isConnected, setIsConnected] = useState(false)
  const [isMuted, setIsMuted] = useState(false)
  const [isRecording, setIsRecording] = useState(false)
  const [volume, setVolume] = useState(70)
  const [connectionStatus, setConnectionStatus] = useState<'idle' | 'connecting' | 'connected' | 'error'>('idle')

  const startCall = async () => {
    setConnectionStatus('connecting')
    try {
      setTimeout(() => {
        setIsConnected(true)
        setConnectionStatus('connected')
        console.log('Connected to AI receptionist')
      }, 2000)
    } catch (error) {
      setConnectionStatus('error')
      console.error('Failed to connect:', error)
    }
  }

  const endCall = () => {
    setIsConnected(false)
    setIsRecording(false)
    setConnectionStatus('idle')
  }

  const toggleRecord = () => {
    setIsRecording(!isRecording)
  }

  const getStatusColor = () => {
    switch (connectionStatus) {
      case 'connected': return 'default'
      case 'connecting': return 'secondary'
      case 'error': return 'destructive'
      default: return 'outline'
    }
  }

  const getStatusText = () => {
    switch (connectionStatus) {
      case 'connected': return '• Connected'
      case 'connecting': return '• Connecting...'
      case 'error': return '• Connection Error'
      default: return '• Ready'
    }
  }

  const getStatusIcon = () => {
    switch (connectionStatus) {
      case 'connected': return <CheckCircle className="w-4 h-4" />
      case 'error': return <AlertCircle className="w-4 h-4" />
      default: return null
    }
  }

  return (
    <div className="max-w-md mx-auto p-6">
      <Card className="p-8 shadow-xl">
        <div className="text-center space-y-6">
          <div className="flex justify-center mb-4">
            <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-2xl shadow-lg">
              GS
            </div>
          </div>
          
          <h1 className="text-2xl font-bold text-gray-900">Glow Beauty Salon</h1>
          <p className="text-gray-600">AI Receptionist</p>
          
          <div className="flex justify-center items-center gap-2">
            {getStatusIcon()}
            <Badge variant={getStatusColor()}>
              {getStatusText()}
            </Badge>
          </div>

          <div className="bg-gray-100 rounded-3xl p-4 mx-auto shadow-lg" style={{ width: '200px' }}>
            <div className="bg-gray-900 rounded-2xl p-2">
              <div className="flex justify-between mb-2">
                <span className="text-white text-xs">9:41 AM</span>
                <Badge variant="secondary" className="text-xs">📶</Badge>
              </div>
              <div className="text-white text-center py-4">
                {isConnected ? (
                  <div className="space-y-1">
                    {isRecording ? (
                      <>
                        <div className="flex items-center justify-center gap-2">
                          <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></div>
                          <p className="text-sm text-green-400">• Recording</p>
                        </div>
                      </>
                    ) : (
                      <p className="text-sm">Ready to respond...</p>
                    )}
                  </div>
                ) : connectionStatus === 'connecting' ? (
                  <div className="space-y-1">
                    <div className="flex items-center justify-center gap-2">
                      <div className="w-2 h-2 bg-yellow-500 rounded-full animate-pulse"></div>
                      <p className="text-sm text-yellow-400">Connecting...</p>
                    </div>
                  </div>
                ) : (
                  <p className="text-sm">Press call to start</p>
                )}
              </div>
              
              <div className="flex justify-center items-center gap-4">
                <button
                  onClick={() => setIsMuted(!isMuted)}
                  className="text-white hover:bg-gray-800 p-2 rounded-full transition-colors"
                >
                  {isMuted ? <MicOff size={16} /> : <Mic size={16} />}
                </button>
                
                <div className="flex justify-center">
                  {isConnected ? (
                    <button
                      onClick={endCall}
                      className="bg-red-500 hover:bg-red-600 p-4 rounded-full transition-all transform hover:scale-105"
                    >
                      <PhoneOff size={20} className="text-white" />
                    </button>
                  ) : (
                    <button
                      onClick={startCall}
                      disabled={connectionStatus === 'connecting'}
                      className={`p-4 rounded-full transition-all transform hover:scale-105 ${
                        connectionStatus === 'connecting' 
                          ? 'bg-yellow-500 hover:bg-yellow-600' 
                          : 'bg-green-500 hover:bg-green-600'
                      }`}
                    >
                      {connectionStatus === 'connecting' ? (
                        <div className="w-5 h-5 border-2 border-t-transparent border-white rounded-full animate-spin"></div>
                      ) : (
                        <Phone size={20} className="text-white" />
                      )}
                    </button>
                  )}
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-2">
            <div className="flex items-center justify-between text-sm text-gray-600">
              <span>Volume</span>
              <span>{volume}%</span>
            </div>
            <Progress value={volume} className="h-2" />
          </div>

          <div className="space-y-3">
            <Button 
              onClick={toggleRecord}
              variant={isRecording ? "destructive" : "secondary"}
              disabled={!isConnected || connectionStatus === 'connecting'}
              className="w-full"
            >
              {isRecording ? (
                <>
                  <MicOff className="w-4 h-4 mr-2" />
                  <span>⏹️ Stop Recording</span>
                </>
              ) : (
                <>
                  <Mic className="w-4 h-4 mr-2" />
                  <span>⏺️ Start Recording</span>
                </>
              )}
            </Button>
            
            <Button 
              variant="outline" 
              className="w-full"
              onClick={() => window.open('http://localhost:8000', '_blank')}
            >
              👨‍💻 Supervisor Dashboard
            </Button>
          </div>

          {isConnected && (
            <div className="flex justify-center gap-2 text-xs text-gray-500">
              <span className="flex items-center gap-1">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span>Connected</span>
              </span>
              <span className="flex items-center gap-1">
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                <span>Voice Active</span>
              </span>
              <span className="flex items-center gap-1">
                <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                <span>AI Ready</span>
              </span>
            </div>
          )}
        </div>
      </Card>
      
      <div className="mt-4 space-y-3">
        {connectionStatus === 'connected' && (
          <Alert variant="success" size="sm">
            <CheckCircle className="h-4 w-4 text-green-600" />
            <div className="grow flex items-center">
              <div>
                <AlertTitle>Connected to AI Receptionist</AlertTitle>
                <AlertDescription>
                  You can now speak with the salon's virtual assistant. Click "Start Recording" to begin.
                </AlertDescription>
              </div>
            </div>
          </Alert>
        )}

        {connectionStatus === 'error' && (
          <Alert variant="error" size="sm">
            <AlertCircle className="h-4 w-4 text-red-600" />
            <div className="grow flex items-center">
              <div>
                <AlertTitle>Connection Failed</AlertTitle>
                <AlertDescription>
                  Unable to connect to the AI receptionist. Please check your internet connection and try again.
                </AlertDescription>
              </div>
            </div>
          </Alert>
        )}
      </div>
      
      {connectionStatus === 'connecting' && (
        <div className="mt-4 text-center space-y-2">
          <Skeleton className="h-2 w-32 mx-auto" />
          <Skeleton className="h-2 w-24 mx-auto" />
          <Skeleton className="h-2 w-40 mx-auto" />
        </div>
      )}
    </div>
  )
}
