import React, { useState, useEffect } from 'react';
import PromptInput from './PromptInput';
import NeuralActivityStream from './NeuralActivityStream';

interface NeuralActivity {
  id: string;
  agent: string;
  action: string;
  timestamp: Date;
  status: 'processing' | 'complete' | 'error';
  details?: string;
  priority: 'low' | 'medium' | 'high' | 'critical';
}

const NeuralCenter: React.FC = () => {
  const [activities, setActivities] = useState<NeuralActivity[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);

  const handlePromptSubmit = (prompt: string) => {
    setIsProcessing(true);
    
    const activityId = Date.now().toString();
    
    // Neural processing simulation with quantum effects
    const processingSteps = [
      {
        delay: 0,
        activity: {
          id: activityId,
          agent: 'Quantum Interface',
          action: 'Prompt received • Initializing quantum processing matrix',
          timestamp: new Date(),
          status: 'processing' as const,
          details: `Input: "${prompt.substring(0, 80)}${prompt.length > 80 ? '...' : ''}"`,
          priority: 'high' as const
        }
      },
      {
        delay: 1200,
        activity: {
          id: Date.now().toString() + '1',
          agent: 'Neural Analyzer',
          action: 'Deep semantic analysis • Extracting intent patterns',
          timestamp: new Date(),
          status: 'processing' as const,
          priority: 'critical' as const
        }
      },
      {
        delay: 2800,
        activity: {
          id: Date.now().toString() + '2',
          agent: 'Task Orchestrator',
          action: 'Decomposing requirements • Generating execution plan',
          timestamp: new Date(),
          status: 'processing' as const,
          priority: 'high' as const
        }
      },
      {
        delay: 4200,
        activity: {
          id: Date.now().toString() + '3',
          agent: 'Neural Analyzer',
          action: 'Analysis complete • Patterns identified successfully',
          timestamp: new Date(),
          status: 'complete' as const,
          details: 'Confidence: 97.3% • Complexity: Medium',
          priority: 'high' as const
        }
      },
      {
        delay: 5000,
        activity: {
          id: Date.now().toString() + '4',
          agent: 'Quantum Coder Alpha',
          action: 'Initializing code synthesis • Loading neural templates',
          timestamp: new Date(),
          status: 'processing' as const,
          priority: 'medium' as const
        }
      },
      {
        delay: 6500,
        activity: {
          id: Date.now().toString() + '5',
          agent: 'Quantum Coder Beta',
          action: 'Parallel processing initiated • Component generation active',
          timestamp: new Date(),
          status: 'processing' as const,
          priority: 'medium' as const
        }
      },
      {
        delay: 8200,
        activity: {
          id: Date.now().toString() + '6',
          agent: 'Neural Tester',
          action: 'Automated testing protocols engaged • Running validation suite',
          timestamp: new Date(),
          status: 'processing' as const,
          priority: 'high' as const
        }
      },
      {
        delay: 10000,
        activity: {
          id: Date.now().toString() + '7',
          agent: 'Quantum System',
          action: 'All neural pathways synchronized • Workflow completed',
          timestamp: new Date(),
          status: 'complete' as const,
          details: 'Success rate: 100% • All agents operational',
          priority: 'critical' as const
        }
      }
    ];

    processingSteps.forEach(({ delay, activity }) => {
      setTimeout(() => {
        setActivities(prev => [activity, ...prev]);
        if (delay === 10000) setIsProcessing(false);
      }, delay);
    });
  };

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-8xl mx-auto">
        {/* Quantum Header */}
        <div className="text-center mb-12 relative">
          <div className="absolute inset-0 quantum-header-bg" />
          <div className="relative z-10">
            <h1 className="text-4xl font-black mb-4 quantum-title-glow">
              <span className="bg-gradient-to-r from-quantum-blue via-quantum-purple to-quantum-pink bg-clip-text text-transparent">
                Neural Command Center
              </span>
            </h1>
            <p className="text-xl text-quantum-blue/90 font-medium tracking-wide">
              Interface with our quantum-enhanced AI collective
            </p>
            <div className="mt-4 flex items-center justify-center space-x-6 text-sm text-quantum-blue/70">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-quantum-green rounded-full animate-pulse" />
                <span>Neural Network: Online</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-quantum-blue rounded-full animate-ping" />
                <span>Quantum Processors: Active</span>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-2 gap-12">
          {/* Neural Input Interface */}
          <div className="space-y-8">
            <PromptInput onSubmit={handlePromptSubmit} isProcessing={isProcessing} />
          </div>

          {/* Quantum Activity Monitor */}
          <div className="space-y-8">
            <NeuralActivityStream activities={activities} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default NeuralCenter;