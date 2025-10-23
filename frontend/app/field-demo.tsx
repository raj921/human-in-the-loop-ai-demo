"use client";

import { Field } from "@ark-ui/react/field";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert";
import { SimpleInput, RequiredInput } from "@/components/ui/field-components";
import { Mail, User, Phone, MessageCircle } from "lucide-react";
import { useState } from "react";

export default function FieldDemo() {
  const [formData, setFormData] = useState({
    personalEmail: "",
    businessEmail: "",
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Form submitted:", formData);
  };

  return (
    <div className="p-8 space-y-8 max-w-4xl mx-auto">
      <div className="text-center">
        <h1 className="text-3xl font-bold mb-2">Field Components Demo</h1>
        <p className="text-gray-600">Ark UI Field components integrated into the salon system</p>
      </div>

      {/* Contact Form for Salon */}
      <Card className="p-6">
        <div className="flex items-center gap-2 mb-6">
          <User className="h-5 w-5 text-blue-600" />
          <h2 className="text-xl font-semibold">Customer Contact Form</h2>
          <Badge variant="secondary">New Component</Badge>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-sm font-medium text-gray-700 mb-2">Personal Details</h3>
              <SimpleInput />
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-700 mb-2">Business Information</h3>
              <RequiredInput />
            </div>
          </div>

          <div className="mt-4 flex gap-4">
            <Button type="submit">Submit Form</Button>
            <Button variant="outline" type="reset">Reset</Button>
          </div>
        </form>
      </Card>

      {/* Supervisor Response Form */}
      <Card className="p-6">
        <div className="flex items-center gap-2 mb-6">
          <Mail className="h-5 w-5 text-purple-600" />
          <h2 className="text-xl font-semibold">Supervisor Response</h2>
          <Badge variant="outline">Integration Example</Badge>
        </div>

        <Alert variant="info">
          <Mail className="h-4 w-4 text-blue-600" />
          <div className="grow flex items-center">
            <div>
              <AlertTitle>Customer Waitlist</AlertTitle>
              <AlertDescription>
                Respond to pending help requests from AI receptionist.
              </AlertDescription>
            </div>
          </div>
        </Alert>

        <div className="mt-6 space-y-4">
          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-700">Contact Email (for follow-up)</label>
            <SimpleInput />
          </div>

          <div className="space-y-2">
            <label className="text-sm font-medium text-gray-700">Response to Customer</label>
            <textarea 
              className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm placeholder-gray-500 focus:border-gray-900 focus:outline-hidden focus:ring-1 focus:ring-gray-900"
              rows={4}
              placeholder="Type your response to the customer..."
            />
          </div>

          <Button size="sm" className="w-full">
            <MessageCircle className="h-4 w-4 mr-2" />
            Send Response
          </Button>
        </div>
      </Card>

      {/* Component Showcase */}
      <Card className="p-6">
        <h2 className="text-xl font-semibold mb-4">Component Features</h2>
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <h3 className="font-medium mb-2">✅ Simple Input</h3>
            <p className="text-sm text-gray-600 mb-3">Basic email input for customer contact</p>
            <SimpleInput />
          </div>
          <div>
            <h3 className="font-medium mb-2">✅ Required Input</h3>
            <p className="text-sm text-gray-600 mb-3">Validated input for business forms</p>
            <RequiredInput />
          </div>
        </div>
      </Card>
    </div>
  );
}
