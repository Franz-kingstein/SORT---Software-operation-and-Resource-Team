import React from 'react';
import { TrendingUp, Clock, AlertTriangle, Target, Zap, Brain, Cpu } from 'lucide-react';

interface MetricsPanelProps {
  metrics: {
    totalTasks: number;
    completedTasks: number;
    activeTasks: number;
    errorRate: number;
    avgProcessingTime: number;
    systemLoad: number;
    quantumCoherence: number;
    neuralSyncRate: number;
  };
}

const MetricsPanel: React.FC<MetricsPanelProps> = ({ metrics }) => {
  const successRate = ((metrics.completedTasks / metrics.totalTasks) * 100).toFixed(1);
  
  const QuantumMetricCard = ({ 
    title, 
    value, 
    unit, 
    icon, 
    gradient, 
    trend,
    isQuantum = false
  }: {
    title: string;
    value: string | number;
    unit?: string;
    icon: React.ReactNode;
    gradient: string;
    trend?: 'up' | 'down' | 'stable';
    isQuantum?: boolean;
  }) => (
    <div className="quantum-metric-card group">
      <div className="flex items-center justify-between mb-4">
        <div className={`quantum-metric-icon bg-gradient-to-br ${gradient}`}>
          <div className="quantum-metric-icon-inner">
            {icon}
          </div>
          <div className="quantum-metric-icon-ring" />
        </div>
        
        {trend && (
          <div className={`quantum-trend-indicator ${
            trend === 'up' ? 'quantum-trend-up' : 
            trend === 'down' ? 'quantum-trend-down' : 
            'quantum-trend-stable'
          }`}>
            <TrendingUp className={`w-4 h-4 ${trend === 'down' ? 'rotate-180' : ''}`} />
          </div>
        )}
      </div>
      
      <div className="space-y-2">
        <div className="flex items-baseline space-x-1">
          <span className={`text-3xl font-black quantum-number-glow ${
            isQuantum ? 'text-quantum-purple' : 'text-white'
          }`}>
            {value}
          </span>
          {unit && (
            <span className="text-sm text-quantum-blue/60 font-medium">
              {unit}
            </span>
          )}
        </div>
        <p className="text-xs text-quantum-blue/70 font-medium tracking-wider uppercase">
          {title}
        </p>
      </div>
      
      {/* Quantum Metric Waves */}
      {isQuantum && (
        <div className="quantum-metric-waves">
          <div className="quantum-metric-wave quantum-metric-wave-1" />
          <div className="quantum-metric-wave quantum-metric-wave-2" />
        </div>
      )}
    </div>
  );

  return (
    <div className="quantum-panel relative overflow-hidden">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center space-x-4 mb-4">
          <div className="quantum-icon-container">
            <Target className="w-6 h-6 text-quantum-orange quantum-pulse" />
            <div className="quantum-icon-ring" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-white quantum-text-glow">
              Quantum Analytics
            </h2>
            <p className="text-quantum-orange/80 font-medium">
              Multi-dimensional performance metrics
            </p>
          </div>
        </div>
        <div className="quantum-divider" />
      </div>

      {/* Metrics Grid */}
      <div className="space-y-6">
        <QuantumMetricCard
          title="Success Rate"
          value={successRate}
          unit="%"
          icon={<Target className="w-5 h-5" />}
          gradient="from-quantum-green to-quantum-emerald"
          trend="up"
        />
        
        <QuantumMetricCard
          title="Processing Time"
          value={metrics.avgProcessingTime}
          unit="sec"
          icon={<Clock className="w-5 h-5" />}
          gradient="from-quantum-blue to-quantum-cyan"
          trend="stable"
        />
        
        <QuantumMetricCard
          title="Error Rate"
          value={metrics.errorRate}
          unit="%"
          icon={<AlertTriangle className="w-5 h-5" />}
          gradient="from-quantum-red to-quantum-orange"
          trend="down"
        />
        
        <QuantumMetricCard
          title="System Load"
          value={metrics.systemLoad}
          unit="%"
          icon={<Cpu className="w-5 h-5" />}
          gradient="from-quantum-purple to-quantum-pink"
          trend="up"
        />

        <QuantumMetricCard
          title="Quantum Coherence"
          value={metrics.quantumCoherence.toFixed(1)}
          unit="%"
          icon={<Zap className="w-5 h-5" />}
          gradient="from-quantum-purple to-quantum-blue"
          trend="stable"
          isQuantum={true}
        />
        
        <QuantumMetricCard
          title="Neural Sync Rate"
          value={metrics.neuralSyncRate.toFixed(1)}
          unit="%"
          icon={<Brain className="w-5 h-5" />}
          gradient="from-quantum-pink to-quantum-purple"
          trend="up"
          isQuantum={true}
        />
      </div>

      {/* Quantum Status Indicator */}
      <div className="mt-8 quantum-status-footer">
        <div className="flex items-center justify-center space-x-3">
          <div className="quantum-live-indicator" />
          <span className="text-xs text-quantum-blue/70 font-mono tracking-wider">
            QUANTUM METRICS • LIVE SYNC • 4.0s REFRESH
          </span>
        </div>
      </div>
    </div>
  );
};

export default MetricsPanel;