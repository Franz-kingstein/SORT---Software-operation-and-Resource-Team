import React, { useState, useEffect } from 'react';
import { Clock, CheckCircle, XCircle, Loader, Zap, Brain } from 'lucide-react';

interface Task {
  id: string;
  title: string;
  status: 'pending' | 'in-progress' | 'completed' | 'failed';
  progress: number;
  assignedAgent: string;
  startTime: Date;
  estimatedCompletion?: Date;
  quantumComplexity: 'low' | 'medium' | 'high' | 'extreme';
  neuralPathways: number;
}

const TaskProgress: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([
    {
      id: '1',
      title: 'Quantum E-commerce Platform',
      status: 'in-progress',
      progress: 82,
      assignedAgent: 'Quantum Coder Alpha',
      startTime: new Date(Date.now() - 2100000),
      estimatedCompletion: new Date(Date.now() + 480000),
      quantumComplexity: 'high',
      neuralPathways: 847
    },
    {
      id: '2',
      title: 'Neural API Integration Suite',
      status: 'in-progress',
      progress: 56,
      assignedAgent: 'Neural Tester Omega',
      startTime: new Date(Date.now() - 1200000),
      estimatedCompletion: new Date(Date.now() + 900000),
      quantumComplexity: 'medium',
      neuralPathways: 423
    },
    {
      id: '3',
      title: 'Quantum Database Architecture',
      status: 'completed',
      progress: 100,
      assignedAgent: 'Neural Analyzer Prime',
      startTime: new Date(Date.now() - 4200000),
      quantumComplexity: 'extreme',
      neuralPathways: 1247
    },
    {
      id: '4',
      title: 'Holographic Authentication System',
      status: 'pending',
      progress: 0,
      assignedAgent: 'Quantum Coder Beta',
      startTime: new Date(),
      quantumComplexity: 'high',
      neuralPathways: 0
    }
  ]);

  // Quantum task simulation
  useEffect(() => {
    const interval = setInterval(() => {
      setTasks(prev => prev.map(task => {
        if (task.status === 'in-progress' && task.progress < 100) {
          const progressIncrease = Math.floor(Math.random() * 8) + 2;
          const newProgress = Math.min(100, task.progress + progressIncrease);
          const newPathways = task.neuralPathways + Math.floor(Math.random() * 50) + 10;
          
          return {
            ...task,
            progress: newProgress,
            neuralPathways: newPathways,
            status: newProgress === 100 ? 'completed' : 'in-progress'
          };
        }
        return task;
      }));
    }, 4000);

    return () => clearInterval(interval);
  }, []);

  const getStatusIcon = (status: Task['status']) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="w-6 h-6 text-quantum-green quantum-glow" />;
      case 'failed':
        return <XCircle className="w-6 h-6 text-quantum-red quantum-glow" />;
      case 'in-progress':
        return <div className="quantum-task-spinner" />;
      default:
        return <Clock className="w-6 h-6 text-quantum-blue/60" />;
    }
  };

  const getComplexityTheme = (complexity: Task['quantumComplexity']) => {
    switch (complexity) {
      case 'extreme': return { color: 'quantum-red', gradient: 'from-quantum-red to-quantum-orange' };
      case 'high': return { color: 'quantum-orange', gradient: 'from-quantum-orange to-quantum-yellow' };
      case 'medium': return { color: 'quantum-yellow', gradient: 'from-quantum-yellow to-quantum-green' };
      default: return { color: 'quantum-green', gradient: 'from-quantum-green to-quantum-emerald' };
    }
  };

  const getStatusTheme = (status: Task['status']) => {
    switch (status) {
      case 'completed': return 'quantum-task-completed';
      case 'failed': return 'quantum-task-failed';
      case 'in-progress': return 'quantum-task-active';
      default: return 'quantum-task-pending';
    }
  };

  return (
    <div className="quantum-panel relative overflow-hidden">
      {/* Header */}
      <div className="mb-8">
        <div className="flex items-center space-x-4 mb-4">
          <div className="quantum-icon-container">
            <Clock className="w-6 h-6 text-quantum-green quantum-pulse" />
            <div className="quantum-icon-ring" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-white quantum-text-glow">
              Quantum Task Timeline
            </h2>
            <p className="text-quantum-green/80 font-medium">
              Multi-dimensional progress tracking
            </p>
          </div>
        </div>
        <div className="quantum-divider" />
      </div>

      {/* Tasks Timeline */}
  <div className="space-y-6 overflow-y-auto quantum-scroll">
        {tasks.map((task, index) => {
          const complexityTheme = getComplexityTheme(task.quantumComplexity);
          const statusTheme = getStatusTheme(task.status);
          
          return (
            <div
              key={task.id}
              className={`quantum-task-card ${statusTheme}`}
              style={{ animationDelay: `${index * 200}ms` }}
            >
              {/* Task Header */}
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-start space-x-4">
                  <div className="quantum-task-icon">
                    {getStatusIcon(task.status)}
                  </div>
                  <div>
                    <h3 className="text-lg font-bold text-white quantum-text-glow mb-1">
                      {task.title}
                    </h3>
                    <div className="flex items-center space-x-4 text-sm">
                      <span className="text-quantum-blue/70">
                        Agent: {task.assignedAgent}
                      </span>
                      <div className={`quantum-complexity-badge bg-gradient-to-r ${complexityTheme.gradient}`}>
                        <span className="text-black font-semibold text-xs">
                          {task.quantumComplexity.toUpperCase()}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
                <span className="text-xs text-quantum-blue/60 font-mono">
                  {task.startTime.toLocaleTimeString()}
                </span>
              </div>

              {/* Quantum Progress Visualization */}
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-quantum-blue/70 font-medium">
                    Quantum Progress
                  </span>
                  <span className="text-sm text-white font-bold">
                    {task.progress}%
                  </span>
                </div>
                
                <div className="quantum-progress-container-large">
                  <div className="quantum-progress-track-large">
                    <div 
                      className="quantum-progress-fill-large"
                      style={{ width: `${task.progress}%` }}
                    >
                      <div className="quantum-progress-glow-large" />
                      <div className="quantum-progress-particles-large" />
                    </div>
                  </div>
                </div>

                {/* Neural Pathways Counter */}
                <div className="flex items-center justify-between text-xs">
                  <div className="flex items-center space-x-2">
                    <Brain className="w-3 h-3 text-quantum-purple" />
                    <span className="text-quantum-purple/70">
                      Neural Pathways: {task.neuralPathways.toLocaleString()}
                    </span>
                  </div>
                  {task.estimatedCompletion && task.status === 'in-progress' && (
                    <span className="text-quantum-green/70">
                      ETA: {task.estimatedCompletion.toLocaleTimeString()}
                    </span>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default TaskProgress;