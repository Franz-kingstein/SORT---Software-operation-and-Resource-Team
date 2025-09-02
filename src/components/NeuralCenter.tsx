import React, { useState, useEffect } from 'react';
import PromptInput from './PromptInput';
import NeuralActivityStream from './NeuralActivityStream';
import { GENERATE_ENDPOINT, HEALTH_ENDPOINT } from '../config';

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
  const [backendStatus, setBackendStatus] = useState<'online' | 'fallback' | 'offline' | 'loading'>('loading');
  const [modelName, setModelName] = useState<string>('');

  // Poll backend /health every 6s
  useEffect(() => {
    let cancelled = false;
    const poll = async () => {
      try {
        const res = await fetch(HEALTH_ENDPOINT, { cache: 'no-store' });
        if (!res.ok) throw new Error(`Status ${res.status}`);
        const data = await res.json();
        if (cancelled) return;
        const status = data.initialized ? 'online' : 'fallback';
        setBackendStatus(status);
        setModelName(data.model_name || (status === 'fallback' ? 'template_fallback' : 'unknown'));
      } catch (e) {
        if (cancelled) return;
        setBackendStatus('offline');
      }
    };
    poll();
    const id = setInterval(poll, 6000);
    return () => { cancelled = true; clearInterval(id); };
  }, []);

  const handlePromptSubmit = async (prompt: string) => {
    setIsProcessing(true);
    const activityId = Date.now().toString();
    // Show initial activity
    setActivities(prev => [{
      id: activityId,
      agent: 'Quantum Interface',
      action: 'Prompt sent to backend',
      timestamp: new Date(),
      status: 'processing',
      details: `Input: "${prompt.substring(0, 80)}${prompt.length > 80 ? '...' : ''}"`,
      priority: 'high'
    }, ...prev]);
    try {
  const response = await fetch(GENERATE_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt, task_type: 'frontend' })
      });
      const data = await response.json();
      setActivities(prev => [{
        id: activityId + '-result',
        agent: 'Backend LLM',
        action: data.success ? 'Code generated successfully' : 'Error generating code',
        timestamp: new Date(),
        status: data.success ? 'complete' : 'error',
        details: data.content || data.error,
        priority: data.success ? 'high' : 'critical'
      }, ...prev]);
    } catch (err) {
      setActivities(prev => [{
        id: activityId + '-error',
        agent: 'Backend LLM',
        action: 'Network or server error',
        timestamp: new Date(),
        status: 'error',
        details: String(err),
        priority: 'critical'
      }, ...prev]);
    }
    setIsProcessing(false);
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
            <div className="mt-4 flex flex-wrap items-center justify-center gap-4 text-sm text-quantum-blue/70">
              <div className="flex items-center space-x-2">
                <div
                  className={`w-2 h-2 rounded-full ${
                    backendStatus === 'online' ? 'bg-quantum-green animate-pulse' :
                    backendStatus === 'fallback' ? 'bg-quantum-yellow animate-pulse' :
                    backendStatus === 'offline' ? 'bg-quantum-red' : 'bg-quantum-blue animate-ping'
                  }`}
                />
                <span>
                  Backend: {backendStatus === 'loading' ? 'Connecting...' : backendStatus === 'online' ? 'Model Active' : backendStatus === 'fallback' ? 'Fallback Mode' : 'Offline'}
                  {modelName && backendStatus !== 'offline' && (
                    <span className="ml-2 text-quantum-blue/50 font-mono">[{modelName}]</span>
                  )}
                </span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-quantum-blue rounded-full animate-ping" />
                <span>Quantum UI: Ready</span>
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