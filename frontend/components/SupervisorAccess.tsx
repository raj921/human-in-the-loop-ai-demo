'use client';

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import { Alert, AlertTitle, AlertDescription } from '@/components/ui/alert'
import { SimpleInput, RequiredInput } from '@/components/ui/field-components'
import { ExternalLink, Users, Clock, Database, TrendingUp, AlertTriangle, CheckCircle, AlertCircle, MessageSquare, Send } from 'lucide-react'

export default function SupervisorAccess() {
  const [stats, setStats] = useState({
    pending: 0,
    total: 0,
    resolved: 0
  });
  const [systemStatus, setSystemStatus] = useState<'loading' | 'online' | 'offline'>('loading');

  // Fetch real stats from backend
  useEffect(() => {
    const fetchStats = async () => {
      try {
        setSystemStatus('loading');
        // In real implementation, fetch from your Python backend
        const response = await fetch('/api/supervisor-stats');
        if (response.ok) {
          const data = await response.json();
          setStats({
            pending: data.pending || 0,
            total: data.total || 0,
            resolved: data.resolved || 0
          });
          setSystemStatus('online');
        }
      } catch (error) {
        console.error('Failed to fetch stats:', error);
        setSystemStatus('offline');
        // Use simulated data if backend is offline
        setStats({
          pending: 2,
          total: 8,
          resolved: 6
        });
      }
    };

    fetchStats();
    const interval = setInterval(fetchStats, 5000); // Refresh every 5 seconds
    return () => clearInterval(interval);
  }, []);

  const needAttention = stats.pending > 0;

  return (
    <Card className="p-6 shadow-xl">
      <div className="space-y-6">
        {/* Header */}
        <div className="text-center">
          <div className="flex items-center justify-center gap-2 mb-2">
            {systemStatus === 'online' ? (
              <CheckCircle className="w-5 h-5 text-green-600" />
            ) : systemStatus === 'loading' ? (
                <div className="w-5 h-5 border-2 border-yellow-400 border-t-transparent rounded-full animate-spin" />
              ) : (
                <AlertCircle className="w-5 h-5 text-red-600" />
              )}
            <h2 className="text-xl font-bold text-gray-900">Supervisor Dashboard</h2>
          </div>
          <p className="text-gray-600">Monitor and respond to help requests</p>
          <Badge variant={systemStatus === 'online' ? 'default' : 'secondary'}>
            {systemStatus === 'online' ? 'Online' : systemStatus === 'loading' ? 'Connecting...' : 'Offline'}
          </Badge>
        </div>

        {/* System Status Alerts */}
        <div className="space-y-3">
          {systemStatus === 'offline' && (
            <Alert variant="error" size="sm">
              <AlertCircle className="h-4 w-4 text-red-600" />
              <div className="grow flex items-center">
                <div>
                  <AlertTitle>Backend Offline</AlertTitle>
                  <AlertDescription>
                    Unable to connect to the salon backend. Some features may not function correctly.
                  </AlertDescription>
                </div>
              </div>
            </Alert>
          )}

          {needAttention && systemStatus === 'online' && (
            <Alert variant="warning" size="sm">
              <AlertTriangle className="h-4 w-4 text-amber-600" />
              <div className="grow flex items-center">
                <div>
                  <AlertTitle>Pending Requests</AlertTitle>
                  <AlertDescription>
                    {stats.pending} customer request{stats.pending > 1 ? 's' : ''} need your attention.
                  </AlertDescription>
                </div>
              </div>
              <Button 
                size="sm" 
                onClick={() => window.open('http://localhost:8000', '_blank')}
              >
                Review
              </Button>
            </Alert>
          )}
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-3 gap-4 text-center">
          <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
            <Users className="h-6 w-6 mx-auto text-blue-600 mb-2" />
            {systemStatus === 'loading' ? (
              <Skeleton className="h-8 w-12 mx-auto" />
            ) : (
              <div className="text-2xl font-bold text-blue-900">{stats.pending}</div>
            )}
            <div className="text-sm text-blue-600">Pending</div>
            {needAttention && (
              <div className="flex items-center justify-center mt-2">
                <AlertTriangle className="w-4 h-4 text-orange-500 mr-1" />
                <span className="text-xs text-orange-600">Needs attention</span>
              </div>
            )}
          </div>
          
          <div className="p-4 bg-green-50 rounded-lg border border-green-200">
            <Clock className="h-6 w-6 mx-auto text-green-600 mb-2" />
            {systemStatus === 'loading' ? (
              <Skeleton className="h-8 w-12 mx-auto" />
            ) : (
              <div className="text-2xl font-bold text-green-900">{stats.total}</div>
            )}
            <div className="text-sm text-green-600">Total Requests</div>
          </div>
          
          <div className="p-4 bg-purple-50 rounded-lg border border-purple-200">
            <Database className="h-6 w-6 mx-auto text-purple-600 mb-2" />
            {systemStatus === 'loading' ? (
              <Skeleton className="h-8 w-12 mx-auto" />
            ) : (
              <div className="text-2xl font-bold text-purple-900">{stats.resolved}</div>
            )}
            <div className="text-sm text-purple-600">Resolved</div>
            <div className="mt-2 flex items-center justify-center">
              <TrendingUp className="w-4 h-4 text-green-500" />
              <span className="text-xs text-green-600">+{stats.resolved > 0 ? Math.round((stats.resolved / stats.total) * 100) : 0}%</span>
            </div>
          </div>
        </div>

        {/* Recent Activity */}
        <div className="space-y-3">
          <h3 className="font-semibold text-gray-900">Recent Activity</h3>
          <div className="space-y-2">
            <div className="flex items-center justify-between p-3 bg-yellow-50 rounded-lg border border-yellow-200">
              <div className="flex items-center gap-2">
                <div className="w-2 h-2 bg-yellow-500 rounded-full"></div>
                <span className="text-sm">New request received</span>
              </div>
              <span className="text-xs text-gray-500">2m ago</span>
            </div>
            
            <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg border border-green-200">
              <div className="flex items-center gap-2">
                <CheckCircle className="w-4 h-4 text-green-600" />
                <span className="text-sm">Request resolved</span>
              </div>
              <span className="text-xs text-gray-500">5m ago</span>
            </div>
          </div>
        </div>

        {/* Response Form */}
        <div className="space-y-3">
          <div className="flex items-center gap-2">
            <MessageSquare className="h-5 w-5 text-blue-600" />
            <h3 className="font-semibold text-gray-900">Quick Response</h3>
          </div>
          
          <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
            <p className="text-sm text-gray-600 mb-3">
              Respond to pending customer requests quickly
            </p>
            
            <div className="space-y-3">
              <div>
                <label className="text-sm font-medium text-gray-700">Customer Email</label>
                <SimpleInput />
              </div>
              
              <div>
                <label className="text-sm font-medium text-gray-700">Your Email (required)</label>
                <RequiredInput />
              </div>
              
              <Button size="sm" className="w-full">
                <Send className="h-4 w-4 mr-2" />
                Send Response
              </Button>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="space-y-3">
          <Badge 
            variant={needAttention ? "destructive" : "default"} 
            className="w-full justify-center py-3"
          >
            {needAttention 
              ? `${stats.pending} requests need attention` 
              : 'All caught up!'
            }
          </Badge>
          
          <div className="grid grid-cols-2 gap-3">
            <Button 
              onClick={() => window.open('http://localhost:8000', '_blank')}
              className="w-full"
            >
              <ExternalLink className="w-4 h-4 mr-2" />
              Full Dashboard
            </Button>
            
            <Button 
              variant="outline" 
              className="w-full"
              onClick={() => window.open('http://localhost:8000/learned-answers', '_blank')}
            >
              <Database className="w-4 h-4 mr-2" />
              Learned Answers
            </Button>
          </div>
        </div>

        {/* System Health */}
        <div className="pt-4 border-t border-gray-200">
          <div className="flex items-center justify-between text-xs text-gray-500">
            <span>Last sync: Just now</span>
            <span>Backend: {systemStatus === 'online' ? 'Connected' : 'Local mode'}</span>
          </div>
        </div>
      </div>
    </Card>
  );
}
