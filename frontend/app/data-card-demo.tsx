"use client";

import SalonDataDisplay from "@/components/ui/data-card-display";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert";
import { TrendingUp, BarChart3, PieChart, Activity, RefreshCw, Settings } from "lucide-react";
import { useState } from "react";

export default function DataCardDemo() {
  const [refreshKey, setRefreshKey] = useState(0);

  const handleRefresh = () => {
    setRefreshKey(prev => prev + 1);
  };

  const handleCardAction = (cardId: string) => {
    console.log(`Card action clicked: ${cardId}`);
    // Here you could navigate to detail pages, open modals, etc.
  };

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto">
      {/* Header */}
      <div className="text-center space-y-4">
        <h1 className="text-4xl font-bold text-foreground">Glow Salon Analytics Dashboard</h1>
        <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
          Real-time business metrics and performance indicators for your beauty salon
        </p>
        <div className="flex justify-center gap-4">
          <Badge variant="secondary" className="px-4 py-2">
            <Activity className="w-4 h-4 mr-2" />
            Live Data
          </Badge>
          <Badge variant="outline" className="px-4 py-2">
            <BarChart3 className="w-4 h-4 mr-2" />
            Analytics
          </Badge>
        </div>
      </div>

      {/* Quick Actions */}
      <Card className="p-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <TrendingUp className="h-6 w-6 text-green-600" />
            <div>
              <h3 className="font-semibold text-foreground">Business Overview</h3>
              <p className="text-sm text-muted-foreground">Key performance indicators for Glow Beauty Salon</p>
            </div>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" size="sm" onClick={handleRefresh}>
              <RefreshCw className="w-4 h-4 mr-2" />
              Refresh
            </Button>
            <Button variant="outline" size="sm">
              <Settings className="w-4 h-4 mr-2" />
              Configure
            </Button>
          </div>
        </div>
      </Card>

      {/* Alert for info */}
      <Alert>
        <TrendingUp className="h-4 w-4 text-blue-600" />
        <div className="grow flex items-center">
          <div>
            <AlertTitle>Performance Insights</AlertTitle>
            <AlertDescription>
              Your salon's AI receptionist is handling 92% of customer inquiries automatically, 
              freeing up your staff to focus on providing exceptional service.
            </AlertDescription>
          </div>
        </div>
      </Alert>

      {/* The main data card display */}
      <div className="space-y-6">
        <div className="flex items-center gap-2">
          <PieChart className="h-5 w-5 text-primary" />
          <h2 className="text-2xl font-semibold text-foreground">Performance Metrics</h2>
        </div>
        
        <SalonDataDisplay key={refreshKey} />
      </div>

      {/* Additional Stats Section */}
      <div className="grid md:grid-cols-2 gap-6">
        <Card className="p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
              <Activity className="h-5 w-5 text-blue-600" />
            </div>
            <h3 className="font-semibold text-foreground">System Health</h3>
          </div>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-sm text-muted-foreground">AI Receptionist</span>
              <Badge variant="default" className="bg-green-500">Online</Badge>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-muted-foreground">Response Time</span>
              <span className="text-sm font-medium">0.8s</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-muted-foreground">Success Rate</span>
              <span className="text-sm font-medium text-green-600">98.5%</span>
            </div>
          </div>
        </Card>

        <Card className="p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className="w-10 h-10 bg-purple-100 rounded-full flex items-center justify-center">
              <BarChart3 className="h-5 w-5 text-purple-600" />
            </div>
            <h3 className="font-semibold text-foreground">Weekly Comparison</h3>
          </div>
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-sm text-muted-foreground">vs Last Week</span>
              <Badge variant="secondary" className="bg-green-100 text-green-800">+15%</Badge>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-muted-foreground">Growth Rate</span>
              <span className="text-sm font-medium text-green-600">18%</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-muted-foreground">Customer Satisfaction</span>
              <span className="text-sm font-medium text-blue-600">4.8/5</span>
            </div>
          </div>
        </Card>
      </div>

      {/* Export Actions */}
      <Card className="p-6 text-center">
        <div className="space-y-4">
          <h3 className="font-semibold text-foreground">Export Reports</h3>
          <p className="text-sm text-muted-foreground">
            Download detailed analytics and performance reports for Glow Beauty Salon
          </p>
          <div className="flex justify-center gap-3">
            <Button variant="outline" onClick={() => handleCardAction('export-pdf')}>
              Export PDF Report
            </Button>
            <Button variant="outline" onClick={() => handleCardAction('export-csv')}>
              Export CSV Data
            </Button>
            <Button onClick={() => handleCardAction('view-full-analytics')}>
              Full Analytics
            </Button>
          </div>
        </div>
      </Card>
    </div>
  );
}
