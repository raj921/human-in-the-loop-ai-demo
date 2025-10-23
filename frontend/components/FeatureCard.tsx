import React from 'react'
import { Card } from '@/components/ui/card'
import { Phone, Users, Database, Brain, Sparkles } from 'lucide-react'

interface FeatureCardProps {
  icon: React.ReactElement;
  title: string;
  description: string;
  color: 'blue' | 'green' | 'purple'
}

export default function FeatureCard({ icon, title, description, color }: FeatureCardProps) {
  const colorClasses = {
    blue: 'from-blue-500 to-blue-600',
    green: 'from-green-500 to-green-600',
    purple: 'from-purple-500 to-purple-600',
  };

  return (
    <Card className="p-8 border-slate-200 hover:border-slate-300 hover:shadow-xl transition-all duration-300 group">
      <div className={`w-14 h-14 bg-gradient-to-br ${colorClasses[color]} rounded-xl flex items-center justify-center mx-auto mb-6 shadow-lg group-hover:scale-110 transition-transform duration-300`}>
        {React.cloneElement(icon, { size: 28, className: 'text-white' })}
      </div>
      <h3 className="font-bold text-slate-900 mb-3 text-lg">{title}</h3>
      <p className="text-sm text-slate-600 leading-relaxed">{description}</p>
    </Card>
  );
}
