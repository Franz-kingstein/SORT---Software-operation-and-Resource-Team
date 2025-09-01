import React, { useState } from 'react';
import { Send, Zap, Sparkles } from 'lucide-react';

interface PromptInputProps {
  onSubmit: (prompt: string) => void;
  isProcessing: boolean;
}

const PromptInput: React.FC<PromptInputProps> = ({ onSubmit, isProcessing }) => {
  const [prompt, setPrompt] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (prompt.trim() && !isProcessing) {
      onSubmit(prompt.trim());
      setPrompt('');
    }
  };

  return (
    <div className="quantum-panel relative overflow-hidden">
      {/* Quantum Energy Field */}
      <div className="absolute inset-0 quantum-energy-field" />
      
      {/* Header Section */}
      <div className="relative z-10 mb-8">
        <div className="flex items-center space-x-4 mb-4">
          <div className="quantum-icon-container">
            <Zap className="w-6 h-6 text-quantum-blue quantum-pulse" />
            <div className="quantum-icon-ring" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-white quantum-text-glow">
              Quantum Command Interface
            </h2>
            <p className="text-quantum-blue/80 font-medium">
              Neural pathway to the AI collective
            </p>
          </div>
        </div>
        
        <div className="quantum-divider" />
        
        <p className="text-quantum-blue/70 text-sm leading-relaxed mt-4">
          Describe your software vision in detail. Our quantum-enhanced AI agents will 
          collaborate across multiple dimensions to manifest your requirements into reality.
        </p>
      </div>

      {/* Quantum Input Form */}
      <form onSubmit={handleSubmit} className="relative z-10 space-y-6">
        <div className="relative quantum-input-container">
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Enter your software requirements... Describe features, architecture, design preferences, and any specific technologies you'd like to use."
            className="quantum-textarea"
            disabled={isProcessing}
            rows={6}
          />
          
          {/* Quantum Border Animation */}
          <div className="absolute inset-0 quantum-border-glow pointer-events-none" />
          
          {/* Character Counter with Quantum Style */}
          <div className="absolute bottom-4 right-4 quantum-counter">
            <span className="text-quantum-blue/60 font-mono text-xs">
              {prompt.length} / 2000
            </span>
          </div>
        </div>

        {/* Quantum Submit Button */}
        <button
          type="submit"
          disabled={!prompt.trim() || isProcessing}
          className={`quantum-submit-button group ${
            !prompt.trim() || isProcessing
              ? 'quantum-button-disabled'
              : 'quantum-button-active'
          }`}
        >
          {/* Button Quantum Field */}
          <div className="absolute inset-0 quantum-button-field" />
          
          {/* Button Content */}
          <div className="relative z-10 flex items-center justify-center space-x-3">
            {isProcessing ? (
              <>
                <div className="quantum-spinner" />
                <span className="font-semibold tracking-wide">
                  Quantum Processing Active...
                </span>
              </>
            ) : (
              <>
                <Send className="w-5 h-5 transition-transform duration-300 group-hover:translate-x-1" />
                <span className="font-semibold tracking-wide">
                  Initiate Neural Synthesis
                </span>
                <Sparkles className="w-4 h-4 opacity-70 group-hover:opacity-100 transition-opacity duration-300" />
              </>
            )}
          </div>
          
          {/* Quantum Ripple Effect */}
          {!isProcessing && prompt.trim() && (
            <div className="absolute inset-0 quantum-ripple opacity-0 group-hover:opacity-100" />
          )}
        </button>
      </form>

      {/* Neural Processing Indicator */}
      {isProcessing && (
        <div className="relative z-10 mt-8 quantum-processing-indicator">
          <div className="flex items-center space-x-4 mb-4">
            <div className="quantum-processing-orb">
              <div className="quantum-core" />
              <div className="quantum-ring-1" />
              <div className="quantum-ring-2" />
              <div className="quantum-ring-3" />
            </div>
            <div>
              <p className="text-quantum-blue font-bold text-lg quantum-text-glow">
                Quantum Neural Network Engaged
              </p>
              <p className="text-quantum-purple/80 text-sm">
                AI agents are synchronizing across quantum dimensions...
              </p>
            </div>
          </div>
          
          {/* Processing Waves */}
          <div className="quantum-processing-waves">
            <div className="quantum-wave quantum-wave-1" />
            <div className="quantum-wave quantum-wave-2" />
            <div className="quantum-wave quantum-wave-3" />
          </div>
        </div>
      )}
    </div>
  );
};

export default PromptInput;