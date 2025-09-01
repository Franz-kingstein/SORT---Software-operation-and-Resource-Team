import React, { useState, useEffect } from 'react';
import SystemHealth from './SystemHealth';
import TaskProgress from './TaskProgress';
import AgentStatus from './AgentStatus';
import MetricsPanel from './MetricsPanel';

const OperationsDashboard: React.FC = () => {
  const [systemMetrics, setSystemMetrics] = useState({
    totalTasks: 247,
    completedTasks: 231,
    activeTasks: 12,
    errorRate: 1.2,
    avgProcessingTime: 38,
    systemLoad: 72,
    quantumCoherence: 94.7,
    neuralSyncRate: 98.3
  });

  // Quantum metrics simulation
  useEffect(() => {
    const interval = setInterval(() => {
      setSystemMetrics(prev => ({
        ...prev,
        systemLoad: Math.floor(Math.random() * 25) + 65,
        activeTasks: Math.floor(Math.random() * 8) + 8,
        quantumCoherence: Math.floor(Math.random() * 10) + 90,
        neuralSyncRate: Math.floor(Math.random() * 5) + 95
      }));
    }, 4000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-8xl mx-auto">
        {/* Quantum Operations Header */}
        <div className="text-center mb-12 relative">
          <div className="absolute inset-0 quantum-header-bg" />
          <div className="relative z-10">
            <h1 className="text-4xl font-black mb-4 quantum-title-glow">
              <span className="bg-gradient-to-r from-quantum-orange via-quantum-red to-quantum-pink bg-clip-text text-transparent">
                Operations Command Hub
              </span>
            </h1>
            <p className="text-xl text-quantum-orange/90 font-medium tracking-wide">
              Monitor quantum systems and neural agent performance
            </p>
            <div className="mt-4 flex items-center justify-center space-x-8 text-sm text-quantum-orange/70">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-quantum-green rounded-full animate-pulse" />
                <span>Quantum Coherence: {systemMetrics.quantumCoherence}%</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-quantum-blue rounded-full animate-ping" />
                <span>Neural Sync: {systemMetrics.neuralSyncRate}%</span>
              </div>
            </div>
          </div>
        </div>

        {/* Operations Grid */}
        <div className="grid grid-cols-1 xl:grid-cols-4 gap-8 mb-8">
          <div className="xl:col-span-3">
            <SystemHealth metrics={systemMetrics} />
          </div>
          <div>
            <MetricsPanel metrics={systemMetrics} />
          </div>
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
          <AgentStatus />
          <TaskProgress />
        </div>
      </div>
    </div>
  );
};

export default OperationsDashboard;