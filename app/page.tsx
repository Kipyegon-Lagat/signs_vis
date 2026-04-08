"use client"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Camera, CameraOff, Volume2, VolumeX } from 'lucide-react'

export default function SignLanguageTranslator() {
  const videoRef = useRef<HTMLVideoElement>(null)
  const canvasRef = useRef<HTMLCanvasElement>(null)
  const [isStreaming, setIsStreaming] = useState(false)
  const [detectedSign, setDetectedSign] = useState("")
  const [confidence, setConfidence] = useState(0)
  const [isProcessing, setIsProcessing] = useState(false)
  const [isSpeechEnabled, setIsSpeechEnabled] = useState(true)
  const [translationHistory, setTranslationHistory] = useState<string[]>([])
  const [backendConnected, setBackendConnected] = useState(false)
  const [connectionError, setConnectionError] = useState("")

  useEffect(() => {
    testBackendConnection()
    const interval = setInterval(testBackendConnection, 5000) // Check every 5 seconds
    return () => clearInterval(interval)
  }, [])

  useEffect(() => {
    let intervalId: NodeJS.Timeout

    if (isStreaming) {
      intervalId = setInterval(() => {
        captureAndAnalyze()
      }, 1000) // Analyze every second
    }

    return () => {
      if (intervalId) {
        clearInterval(intervalId)
      }
    }
  }, [isStreaming])

  const testBackendConnection = async () => {
    try {
      const response = await fetch("http://localhost:8000/")
      if (response.ok) {
        setBackendConnected(true)
        setConnectionError("")
      } else {
        setBackendConnected(false)
        setConnectionError("Backend server responded with error")
      }
    } catch (error) {
      setBackendConnected(false)
      setConnectionError("Cannot connect to backend server. Make sure it's running on port 8000.")
    }
  }

  const startCamera = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: 640, height: 480 },
      })

      if (videoRef.current) {
        videoRef.current.srcObject = stream
        setIsStreaming(true)
      }
    } catch (error) {
      console.error("Error accessing camera:", error)
      alert("Unable to access camera. Please ensure you have granted camera permissions.")
    }
  }

  const stopCamera = () => {
    if (videoRef.current?.srcObject) {
      const stream = videoRef.current.srcObject as MediaStream
      stream.getTracks().forEach((track) => track.stop())
      videoRef.current.srcObject = null
    }
    setIsStreaming(false)
    setDetectedSign("")
    setConfidence(0)
  }

  const captureAndAnalyze = async () => {
    if (!videoRef.current || !canvasRef.current || isProcessing) return

    setIsProcessing(true)

    const canvas = canvasRef.current
    const video = videoRef.current
    const ctx = canvas.getContext("2d")

    if (!ctx) return

    // Set canvas dimensions to match video
    canvas.width = video.videoWidth
    canvas.height = video.videoHeight

    // Draw current video frame to canvas
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height)

    // Convert canvas to blob
    canvas.toBlob(
      async (blob) => {
        if (!blob) return

        try {
          const formData = new FormData()
          formData.append("image", blob, "frame.jpg")

          const response = await fetch("/api/detect-sign", {
            method: "POST",
            body: formData,
          })

          if (response.ok) {
            const result = await response.json()

            if (result.sign && result.confidence > 0.7) {
              setDetectedSign(result.sign)
              setConfidence(result.confidence)

              // Add to history if it's a new detection
              if (result.sign !== detectedSign) {
                setTranslationHistory((prev) => [result.sign, ...prev.slice(0, 9)])

                // Text-to-speech
                if (isSpeechEnabled && "speechSynthesis" in window) {
                  const utterance = new SpeechSynthesisUtterance(result.sign)
                  utterance.rate = 0.8
                  utterance.volume = 0.7
                  speechSynthesis.speak(utterance)
                }
              }
            }
          }
        } catch (error) {
          console.error("Error analyzing frame:", error)
        } finally {
          setIsProcessing(false)
        }
      },
      "image/jpeg",
      0.8,
    )
  }

  const toggleSpeech = () => {
    setIsSpeechEnabled(!isSpeechEnabled)
    if (!isSpeechEnabled) {
      speechSynthesis.cancel()
    }
  }

  const speakText = (text: string) => {
    if ("speechSynthesis" in window) {
      const utterance = new SpeechSynthesisUtterance(text)
      utterance.rate = 0.8
      utterance.volume = 0.7
      speechSynthesis.speak(utterance)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">Sign Language Translator</h1>
          <p className="text-lg text-gray-600">Real-time sign language detection and translation</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Camera Feed */}
          <div className="lg:col-span-2">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center justify-between">
                  <span>Camera Feed</span>
                  <div className="flex items-center gap-2">
                    <Badge variant={backendConnected ? "default" : "destructive"}>
                      {backendConnected ? "Backend Connected" : "Backend Disconnected"}
                    </Badge>
                    <Button onClick={toggleSpeech} variant="outline" size="sm">
                      {isSpeechEnabled ? <Volume2 className="h-4 w-4" /> : <VolumeX className="h-4 w-4" />}
                    </Button>
                    <Button
                      onClick={isStreaming ? stopCamera : startCamera}
                      variant={isStreaming ? "destructive" : "default"}
                      disabled={!backendConnected}
                    >
                      {isStreaming ? (
                        <>
                          <CameraOff className="h-4 w-4 mr-2" />
                          Stop Camera
                        </>
                      ) : (
                        <>
                          <Camera className="h-4 w-4 mr-2" />
                          Start Camera
                        </>
                      )}
                    </Button>
                  </div>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="relative">
                  <video
                    ref={videoRef}
                    autoPlay
                    playsInline
                    muted
                    className="w-full h-auto rounded-lg bg-gray-900"
                    style={{ maxHeight: "480px" }}
                  />
                  <canvas ref={canvasRef} className="hidden" />
                  {isProcessing && (
                    <div className="absolute top-4 right-4">
                      <Badge variant="secondary">Processing...</Badge>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Detection Results */}
          <div className="space-y-6">
            {!backendConnected && connectionError && (
              <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-red-800 font-medium">Backend Connection Issue</p>
                <p className="text-red-600 text-sm">{connectionError}</p>
                <p className="text-red-600 text-sm mt-2">
                  Please run: <code className="bg-red-100 px-1 rounded">python scripts/simple_server.py</code>
                </p>
              </div>
            )}
            {/* Current Detection */}
            <Card>
              <CardHeader>
                <CardTitle>Current Detection</CardTitle>
              </CardHeader>
              <CardContent>
                {detectedSign ? (
                  <div className="text-center">
                    <div className="text-3xl font-bold text-blue-600 mb-2">{detectedSign}</div>
                    <div className="text-sm text-gray-500 mb-4">Confidence: {Math.round(confidence * 100)}%</div>
                    <Button onClick={() => speakText(detectedSign)} variant="outline" size="sm">
                      <Volume2 className="h-4 w-4 mr-2" />
                      Speak
                    </Button>
                  </div>
                ) : (
                  <div className="text-center text-gray-500">
                    {isStreaming ? "Watching for signs..." : "Start camera to begin detection"}
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Translation History */}
            <Card>
              <CardHeader>
                <CardTitle>Recent Translations</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2 max-h-64 overflow-y-auto">
                  {translationHistory.length > 0 ? (
                    translationHistory.map((sign, index) => (
                      <div
                        key={index}
                        className="flex items-center justify-between p-2 bg-gray-50 rounded cursor-pointer hover:bg-gray-100"
                        onClick={() => speakText(sign)}
                      >
                        <span className="font-medium">{sign}</span>
                        <Volume2 className="h-4 w-4 text-gray-400" />
                      </div>
                    ))
                  ) : (
                    <div className="text-center text-gray-500 py-4">No translations yet</div>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Instructions */}
            <Card>
              <CardHeader>
                <CardTitle>How to Use</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-2 text-sm text-gray-600">
                  <p>1. Click "Start Camera" to begin</p>
                  <p>2. Position your hand clearly in view</p>
                  <p>3. Make sign language gestures</p>
                  <p>4. Watch for real-time translations</p>
                  <p>5. Click translations to hear them spoken</p>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}
