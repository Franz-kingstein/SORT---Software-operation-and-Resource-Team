import React, { useEffect, useRef } from 'react';
import { Brain, Code, TestTube, CheckCircle, AlertTriangle, Activity, Zap, Cpu } from 'lucide-react';

interface NeuralActivity {
  id: string;
  agent: string;
  action: string;
  timestamp: Date;
  status: 'processing' | 'complete' | 'error';
  details?: string;
  priority: 'low' | 'medium' | 'high' | 'critical';
}

interface NeuralActivityStreamProps {
  activities: NeuralActivity[];
}

const getAgentIcon = (agent: string) => {
  if (agent.includes('Neural') || agent.includes('Analyzer')) return <Brain className="w-5 h-5" />;
  if (agent.includes('Coder')) return <Code className="w-5 h-5" />;
  if (agent.includes('Tester')) return <TestTube className="w-5 h-5" />;
  if (agent.includes('Orchestrator')) return <Cpu className="w-5 h-5" />;
  if (agent.includes('Quantum')) return <Zap className="w-5 h-5" />;
  return <Activity className="w-5 h-5" />;
};

const getStatusIcon = (status: string) => {
  switch (status) {
    case 'complete':
      return <CheckCircle className="w-5 h-5 text-quantum-green quantum-glow" />;
    case 'error':
      return <AlertTriangle className="w-5 h-5 text-quantum-red quantum-glow" />;
    default:
      return <div className="quantum-status-spinner" />;
  }
};

const getAgentTheme = (agent: string) => {
  if (agent.includes('Neural') || agent.includes('Analyzer')) 
    return { gradient: 'from-quantum-purple to-quantum-pink', color: 'quantum-purple' };
  if (agent.includes('Coder')) 
    return { gradient: 'from-quantum-blue to-quantum-cyan', color: 'quantum-blue' };
  if (agent.includes('Tester')) 
    return { gradient: 'from-quantum-green to-quantum-emerald', color: 'quantum-green' };
  if (agent.includes('Orchestrator')) 
    return { gradient: 'from-quantum-orange to-quantum-yellow', color: 'quantum-orange' };
  if (agent.includes('Quantum')) 
    return { gradient: 'from-quantum-pink to-quantum-purple', color: 'quantum-pink' };
  return { gradient: 'from-quantum-blue to-quantum-purple', color: 'quantum-blue' };
};

const getPriorityIndicator = (priority: string) => {
  switch (priority) {
    case 'critical': return 'quantum-priority-critical';
    case 'high': return 'quantum-priority-high';
    case 'medium': return 'quantum-priority-medium';
    default: return 'quantum-priority-low';
  }
};

const NeuralActivityStream: React.FC<NeuralActivityStreamProps> = ({ activities }) => {
  const streamRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (streamRef.current) {
      streamRef.current.scrollTop = 0;
    }
  }, [activities]);

  return (
    <div className="quantum-panel relative overflow-hidden">
      {/* Quantum Stream Header */}
      <div className="mb-8">
        <div className="flex items-center space-x-4 mb-4">
          <div className="quantum-icon-container">
            <Activity className="w-6 h-6 text-quantum-green quantum-pulse" />
            <div className="quantum-icon-ring" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-white quantum-text-glow">
              Neural Activity Stream
            </h2>
            <p className="text-quantum-green/80 font-medium">
              Real-time quantum consciousness monitoring
            </p>
          </div>
        </div>
        
        <div className="quantum-divider" />
      </div>

      {/* Activity Stream Container */}
      <div 
        ref={streamRef}
        className="h-[600px] overflow-y-auto quantum-scroll space-y-4"
      >
        {activities.length === 0 ? (
          <div className="h-full flex items-center justify-center">
            <div className="text-center quantum-waiting-state">
              <div className="quantum-waiting-orb mb-6">
                <div className="quantum-core-waiting" />
                <div className="quantum-ring-waiting-1" />
                <div className="quantum-ring-waiting-2" />
                <div className="quantum-ring-waiting-3" />
              </div>
              <p className="text-quantum-blue/80 text-lg font-medium">
                Quantum neural pathways ready...
              </p>
              <p className="text-quantum-blue/50 text-sm mt-2">
                Awaiting consciousness input
              </p>
            </div>
          </div>
        ) : (
          activities.map((activity, index) => {
            const theme = getAgentTheme(activity.agent);
            return (
              <div
                key={activity.id}
                className={`quantum-activity-card ${index === 0 ? 'quantum-slide-in' : ''}`}
                style={{ animationDelay: `${index * 100}ms` }}
              >
                {/* Priority Indicator */}
                <div className={`quantum-priority-bar ${getPriorityIndicator(activity.priority)}`} />
                
                <div className="flex items-start space-x-4 p-6">
                  {/* Agent Avatar */}
                  <div className={`quantum-agent-avatar bg-gradient-to-br ${theme.gradient}`}>
                    <div className="quantum-avatar-inner">
                      {getAgentIcon(activity.agent)}
                    </div>
                    <div className="quantum-avatar-ring" />
                  </div>
                  
                  <div className="flex-1 min-w-0">
                    {/* Header */}
                    <div className="flex items-center justify-between mb-3">
                      <div>
                        <h3 className={`font-bold text-${theme.color} quantum-text-glow text-lg`}>
                          {activity.agent}
                        </h3>
                        <p className="text-xs text-quantum-blue/60 font-mono tracking-wider uppercase">
                          Agent ID: {activity.agent.replace(/\s+/g, '-').toLowerCase()}
                        </p>
                      </div>
                      <div className="flex items-center space-x-3">
                        {getStatusIcon(activity.status)}
                        <span className="text-xs text-quantum-blue/70 font-mono">
                          {activity.timestamp.toLocaleTimeString()}
                        </span>
                      </div>
                    </div>
                    
                    {/* Action Description */}
                    <div className="quantum-action-container mb-4">
                      <p className="text-white font-medium leading-relaxed">
                        {activity.action}
                      </p>
                    </div>
                    
                    {/* Details Panel */}
                    {activity.details && (
                      <div className="quantum-details-panel">
                        <p className="text-quantum-blue/80 text-sm font-mono leading-relaxed">
                          {activity.details}
                        </p>
                      </div>
                    )}
                  </div>
                </div>

                {/* Quantum Activity Waves */}
                {activity.status === 'processing' && (
                  <div className="quantum-activity-waves">
                    <div className="quantum-wave-activity quantum-wave-activity-1" />
                    <div className="quantum-wave-activity quantum-wave-activity-2" />
                    <div className="quantum-wave-activity quantum-wave-activity-3" />
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};

export default NeuralActivityStream;