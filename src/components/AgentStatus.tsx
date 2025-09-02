import React, { useState, useEffect } from 'react';
import { Brain, Code, TestTube, Zap, Cpu, Circle } from 'lucide-react';

interface Agent {
  id: string;
  name: string;
  status: 'online' | 'busy' | 'offline' | 'quantum-sync';
  currentTask?: string;
  tasksCompleted: number;
  avgResponseTime: number;
  quantumEfficiency: number;
  neuralLoad: number;
}

const AgentStatus: React.FC = () => {
  const [agents, setAgents] = useState<Agent[]>([
    {
      id: '1',
      name: 'Neural Analyzer Prime',
      status: 'quantum-sync',
      currentTask: 'Deep semantic pattern analysis',
      tasksCompleted: 67,
      avgResponseTime: 1.8,
      quantumEfficiency: 97.2,
      neuralLoad: 45
    },
    {
      id: '2',
      name: 'Quantum Coder Alpha',
      status: 'busy',
      currentTask: 'Synthesizing React components with quantum algorithms',
      tasksCompleted: 52,
      avgResponseTime: 8.4,
      quantumEfficiency: 94.8,
      neuralLoad: 78
    },
    {
      id: '3',
      name: 'Quantum Coder Beta',
      status: 'online',
      tasksCompleted: 48,
      avgResponseTime: 7.9,
      quantumEfficiency: 96.1,
      neuralLoad: 23
    },
    {
      id: '4',
      name: 'Neural Tester Omega',
      status: 'busy',
      currentTask: 'Quantum validation protocols active',
      tasksCompleted: 41,
      avgResponseTime: 5.2,
      quantumEfficiency: 98.7,
      neuralLoad: 67
    }
  ]);

  // Quantum agent simulation
  useEffect(() => {
    const interval = setInterval(() => {
      setAgents(prev => prev.map(agent => {
        const statuses: Agent['status'][] = ['online', 'busy', 'offline', 'quantum-sync'];
        const shouldUpdate = Math.random() > 0.6;
        
        if (shouldUpdate) {
          const newStatus = statuses[Math.floor(Math.random() * statuses.length)];
          const efficiencyChange = (Math.random() - 0.5) * 2;
          const loadChange = (Math.random() - 0.5) * 20;
          
          return {
            ...agent,
            status: newStatus,
            quantumEfficiency: Math.max(85, Math.min(100, agent.quantumEfficiency + efficiencyChange)),
            neuralLoad: Math.max(0, Math.min(100, agent.neuralLoad + loadChange)),
            tasksCompleted: agent.status === 'busy' && Math.random() > 0.7 
              ? agent.tasksCompleted + 1 
              : agent.tasksCompleted
          };
        }
        return agent;
      }));
    }, 6000);

    return () => clearInterval(interval);
  }, []);

  const getAgentIcon = (name: string) => {
    if (name.includes('Neural') || name.includes('Analyzer')) return <Brain className="w-5 h-5" />;
    if (name.includes('Coder')) return <Code className="w-5 h-5" />;
    if (name.includes('Tester')) return <TestTube className="w-5 h-5" />;
    return <Cpu className="w-5 h-5" />;
  };

  const getStatusTheme = (status: Agent['status']) => {
    switch (status) {
      case 'online': 
        return { 
          color: 'text-quantum-green', 
          bg: 'quantum-status-online',
          dot: 'quantum-dot-online'
        };
      case 'busy': 
        return { 
          color: 'text-quantum-yellow', 
          bg: 'quantum-status-busy',
          dot: 'quantum-dot-busy'
        };
      case 'quantum-sync': 
        return { 
          color: 'text-quantum-purple', 
          bg: 'quantum-status-sync',
          dot: 'quantum-dot-sync'
        };
      default: 
        return { 
          color: 'text-quantum-red', 
          bg: 'quantum-status-offline',
          dot: 'quantum-dot-offline'
        };
    }
  };

  const getAgentTheme = (name: string) => {
    if (name.includes('Neural')) return 'from-quantum-purple to-quantum-pink';
    if (name.includes('Alpha')) return 'from-quantum-blue to-quantum-cyan';
    if (name.includes('Beta')) return 'from-quantum-cyan to-quantum-green';
    if (name.includes('Omega')) return 'from-quantum-green to-quantum-emerald';
    return 'from-quantum-orange to-quantum-red';
  };

  return (
    <div className="quantum-panel relative overflow-hidden">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center space-x-4 mb-4">
          <div className="quantum-icon-container">
            <Brain className="w-6 h-6 text-quantum-purple quantum-pulse" />
            <div className="quantum-icon-ring" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-white quantum-text-glow">
              Neural Agent Matrix
            </h2>
            <p className="text-quantum-purple/80 font-medium">
              Quantum consciousness monitoring system
            </p>
          </div>
        </div>
        <div className="quantum-divider" />
      </div>

      {/* Agents Grid */}
      <div className="space-y-6">
        {agents.map((agent, index) => {
          const statusTheme = getStatusTheme(agent.status);
          const agentTheme = getAgentTheme(agent.name);
          
          return (
            <div
              key={agent.id}
              className="quantum-agent-card"
              style={{ animationDelay: `${index * 150}ms` }}
            >
              <div className="flex items-start space-x-4 p-6">
                {/* Agent Quantum Avatar */}
                <div className={`quantum-agent-avatar-large bg-gradient-to-br ${agentTheme}`}>
                  <div className="quantum-avatar-inner-large">
                    {getAgentIcon(agent.name)}
                  </div>
                  <div className="quantum-avatar-ring-large" />
                  <div className={`quantum-status-indicator ${statusTheme.dot}`} />
                </div>
                
                <div className="flex-1 min-w-0">
                  {/* Agent Header */}
                  <div className="flex items-center justify-between mb-3">
                    <div>
                      <h3 className="text-lg font-bold text-white quantum-text-glow">
                        {agent.name}
                      </h3>
                      <div className="flex items-center space-x-3 mt-1">
                        <span className={`text-sm font-semibold ${statusTheme.color} tracking-wider uppercase`}>
                          {agent.status.replace('-', ' ')}
                        </span>
                        {agent.currentTask && (
                          <span className="text-xs text-quantum-blue/70 font-mono">
                            • {agent.currentTask}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Quantum Metrics */}
                  <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-4">
                    <div className="quantum-mini-metric">
                      <p className="text-quantum-blue/70 text-xs font-medium">Tasks</p>
                      <p className="text-white font-bold text-lg">{agent.tasksCompleted}</p>
                    </div>
                    <div className="quantum-mini-metric">
                      <p className="text-quantum-green/70 text-xs font-medium">Response</p>
                      <p className="text-white font-bold text-lg">{agent.avgResponseTime}s</p>
                    </div>
                    <div className="quantum-mini-metric">
                      <p className="text-quantum-purple/70 text-xs font-medium">Efficiency</p>
                      <p className="text-white font-bold text-lg">{agent.quantumEfficiency.toFixed(1)}%</p>
                    </div>
                    <div className="quantum-mini-metric">
                      <p className="text-quantum-orange/70 text-xs font-medium">Neural Load</p>
                      <p className="text-white font-bold text-lg">{agent.neuralLoad}%</p>
                    </div>
                  </div>

                  {/* Quantum Efficiency Bar */}
                  <div className="quantum-efficiency-container">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-xs text-quantum-blue/70 font-medium">
                        Quantum Efficiency
                      </span>
                      <span className="text-xs text-white font-mono">
                        {agent.quantumEfficiency.toFixed(1)}%
                      </span>
                    </div>
                    <div className="quantum-efficiency-track">
                      <div 
                        className="quantum-efficiency-fill"
                        style={{ width: `${agent.quantumEfficiency}%` }}
                      >
                        <div className="quantum-efficiency-glow" />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default AgentStatus;