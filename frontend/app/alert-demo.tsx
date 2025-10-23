"use client";

import { Alert, AlertTitle, AlertDescription, AlertContent } from "@/components/ui/alert";
import { Button } from "@/components/ui/button";
import { AlertTriangle, CheckCircle, Info, XCircle, AlertCircle } from "lucide-react";
import { useState } from "react";

export default function AlertDemo() {
  const [dismissed, setDismissed] = useState(false);

  return (
    <div className="p-8 space-y-6 max-w-2xl mx-auto">
      <h1 className="text-3xl font-bold mb-8">Alert Component Demo</h1>
      
      {/* Success Alert */}
      <Alert variant="success">
        <CheckCircle className="h-4 w-4 text-green-600" />
        <div className="grow flex items-center">
          <div>
            <AlertTitle>Success!</AlertTitle>
            <AlertDescription>
              Your connection to the AI receptionist has been established successfully.
            </AlertDescription>
          </div>
        </div>
      </Alert>

      {/* Error Alert */}
      <Alert variant="error">
        <XCircle className="h-4 w-4 text-red-600" />
        <div className="grow flex items-center">
          <div>
            <AlertTitle>Connection Failed</AlertTitle>
            <AlertDescription>
              Unable to connect to the salon backend. Please check your network connection.
            </AlertDescription>
          </div>
        </div>
      </Alert>

      {/* Warning Alert */}
      <Alert variant="warning">
        <AlertTriangle className="h-4 w-4 text-amber-600" />
        <div className="grow flex items-center">
          <div>
            <AlertTitle>Microphone Access</AlertTitle>
            <AlertDescription>
              Microphone permission is required for voice conversation with the AI.
            </AlertDescription>
          </div>
        </div>
        <Button size="sm" variant="outline">
          Enable
        </Button>
      </Alert>

      {/* Info Alert */}
      <Alert variant="info">
        <Info className="h-4 w-4 text-blue-600" />
        <div className="grow flex items-center">
          <div>
            <AlertTitle>New Feature</AlertTitle>
            <AlertDescription>
              Smart escalation to human supervisors is now active when AI can't answer.
            </AlertDescription>
          </div>
        </div>
      </Alert>

      {/* Default Alert */}
      <Alert>
        <AlertCircle className="h-4 w-4" />
        <div className="grow flex items-center">
          <AlertDescription>
            This is a default styled alert message.
          </AlertDescription>
        </div>
      </Alert>

      {/* Complex Layout Alert */}
      <Alert variant="success" size="lg" layout="complex">
        <CheckCircle className="h-6 w-6 text-green-600 mt-0.5" />
        <div className="grow">
          <AlertTitle>AI Training Complete</AlertTitle>
          <AlertDescription>
            The system has successfully learned from 15 previous supervisor responses 
            and now handles 85% more customer inquiries without escalation.
          </AlertDescription>
        </div>
        <Button size="sm">View Details</Button>
      </Alert>

      {/* Dismissible Alert */}
      {!dismissed && (
        <Alert variant="info" className="relative">
          <Info className="h-4 w-4 text-blue-600" />
          <div className="grow flex items-center">
            <div>
              <AlertTitle>System Update</AlertTitle>
              <AlertDescription>
                New response templates have been added to the knowledge base.
              </AlertDescription>
            </div>
          </div>
          <Button 
            size="sm" 
            variant="ghost"
            onClick={() => setDismissed(true)}
          >
            ×
          </Button>
        </Alert>
      )}
    </div>
  );
}
