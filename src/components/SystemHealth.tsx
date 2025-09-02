import React from 'react';
import { Server, Cpu, MemoryStick as Memory, HardDrive, Wifi, Zap, CheckCircle, Activity, Brain } from 'lucide-react';

interface SystemHealthProps {
  metrics: {
    systemLoad: number;
    totalTasks: number;
    completedTasks: number;
    activeTasks: number;
    quantumCoherence: number;
    neuralSyncRate: number;
  };
}

const SystemHealth: React.FC<SystemHealthProps> = ({ metrics }) => {
  const cpuUsage = metrics.systemLoad;
  const memoryUsage = Math.floor(Math.random() * 25) + 55;
  const diskUsage = Math.floor(Math.random() * 15) + 30;
  const networkStatus = 98;

  const getQuantumColor = (value: number) => {
    if (value < 50) return 'from-quantum-red to-quantum-orange';
    if (value < 80) return 'from-quantum-yellow to-quantum-orange';
    return 'from-quantum-green to-quantum-emerald';
  };

  const QuantumHealthBar = ({ 
    label, 
    value, 
    icon, 
    maxValue = 100 
  }: { 
    label: string; 
    value: number; 
    icon: React.ReactNode; 
    maxValue?: number;
  }) => (
    <div className="quantum-health-metric">
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center space-x-3">
          <div className="quantum-metric-icon">
            {icon}
            <div className="quantum-icon-pulse" />
          </div>
          <span className="font-semibold text-white quantum-text-glow">
            {label}
          </span>
        </div>
        <div className="quantum-value-display">
          <span className="text-lg font-bold text-quantum-blue">
            {value}%
          </span>
        </div>
      </div>
      
      <div className="quantum-progress-container">
        <div className="quantum-progress-track">
          <div 
            className={`quantum-progress-fill bg-gradient-to-r ${getQuantumColor(value)}`}
            style={{ width: `${(value / maxValue) * 100}%` }}
          >
            <div className="quantum-progress-glow" />
            <div className="quantum-progress-particles" />
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="quantum-panel relative overflow-hidden">
      {/* Quantum Field Background */}
      <div className="absolute inset-0 quantum-health-field" />
      
      {/* Header */}
      <div className="relative z-10 mb-8">
        <div className="flex items-center space-x-4 mb-4">
          <div className="quantum-icon-container">
            <Server className="w-6 h-6 text-quantum-orange quantum-pulse" />
            <div className="quantum-icon-ring" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-white quantum-text-glow">
              Quantum System Health
            </h2>
            <p className="text-quantum-orange/80 font-medium">
              Real-time dimensional resource monitoring
            </p>
          </div>
        </div>
        <div className="quantum-divider" />
      </div>

      {/* Health Metrics Grid */}
      <div className="relative z-10 grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <QuantumHealthBar 
          label="Quantum CPU Cores" 
          value={cpuUsage} 
          icon={<Cpu className="w-5 h-5" />}
        />
        <QuantumHealthBar 
          label="Neural Memory Banks" 
          value={memoryUsage} 
          icon={<Memory className="w-5 h-5" />}
        />
        <QuantumHealthBar 
          label="Data Storage Matrix" 
          value={diskUsage} 
          icon={<HardDrive className="w-5 h-5" />}
        />
        <QuantumHealthBar 
          label="Quantum Network" 
          value={networkStatus} 
          icon={<Wifi className="w-5 h-5" />}
        />
      </div>

      {/* Quantum System Stats */}
      <div className="relative z-10 grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="quantum-stat-card">
          <div className="quantum-stat-icon bg-gradient-to-r from-quantum-blue to-quantum-cyan">
            <Zap className="w-5 h-5" />
          </div>
          <div className="quantum-stat-content">
            <p className="text-3xl font-black text-quantum-blue quantum-number-glow">
              {metrics.totalTasks}
            </p>
            <p className="text-xs text-quantum-blue/70 font-medium tracking-wider uppercase">
              Total Operations
            </p>
          </div>
        </div>
        
        <div className="quantum-stat-card">
          <div className="quantum-stat-icon bg-gradient-to-r from-quantum-green to-quantum-emerald">
            <CheckCircle className="w-5 h-5" />
          </div>
          <div className="quantum-stat-content">
            <p className="text-3xl font-black text-quantum-green quantum-number-glow">
              {metrics.completedTasks}
            </p>
            <p className="text-xs text-quantum-green/70 font-medium tracking-wider uppercase">
              Completed
            </p>
          </div>
        </div>
        
        <div className="quantum-stat-card">
          <div className="quantum-stat-icon bg-gradient-to-r from-quantum-yellow to-quantum-orange">
            <Activity className="w-5 h-5" />
          </div>
          <div className="quantum-stat-content">
            <p className="text-3xl font-black text-quantum-yellow quantum-number-glow">
              {metrics.activeTasks}
            </p>
            <p className="text-xs text-quantum-yellow/70 font-medium tracking-wider uppercase">
              Active Tasks
            </p>
          </div>
        </div>
        
        <div className="quantum-stat-card">
          <div className="quantum-stat-icon bg-gradient-to-r from-quantum-purple to-quantum-pink">
            <Brain className="w-5 h-5" />
          </div>
          <div className="quantum-stat-content">
            <p className="text-3xl font-black text-quantum-purple quantum-number-glow">
              {metrics.quantumCoherence.toFixed(1)}%
            </p>
            <p className="text-xs text-quantum-purple/70 font-medium tracking-wider uppercase">
              Coherence
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SystemHealth;