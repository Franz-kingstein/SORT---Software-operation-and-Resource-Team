import React from 'react';
import { Brain, Activity, Zap } from 'lucide-react';

interface NavigationProps {
  currentPage: 'neural' | 'operations';
  onPageChange: (page: 'neural' | 'operations') => void;
}

const Navigation: React.FC<NavigationProps> = ({ currentPage, onPageChange }) => {
  return (
    <nav className="fixed top-0 left-0 right-0 z-50 quantum-glass border-b border-quantum-blue/30">
      <div className="max-w-7xl mx-auto px-4 py-2">
        <div className="flex items-center justify-between">
          {/* Quantum Logo */}
          <div className="flex items-center space-x-2">
            <div className="relative w-8 h-8 quantum-logo-container">
              <div className="absolute inset-0 quantum-orb bg-gradient-to-r from-quantum-blue via-quantum-purple to-quantum-pink rounded-full" />
              <div className="absolute inset-1 bg-black rounded-full flex items-center justify-center">
                <Brain className="w-4 h-4 text-quantum-blue quantum-glow" />
              </div>
              <div className="absolute inset-0 quantum-ring" />
            </div>
            <div className="quantum-text-glow">
              <h1 className="text-lg font-black bg-gradient-to-r from-quantum-blue via-quantum-purple to-quantum-pink bg-clip-text text-transparent">
                SORT
              </h1>
              <p className="text-[10px] text-quantum-blue/80 font-medium tracking-wider uppercase">
                Software Operation & Resource Team
              </p>
            </div>
          </div>

          {/* Quantum Navigation */}
          <div className="flex space-x-1 p-1 quantum-nav-container rounded-xl">
            <button
              onClick={() => onPageChange('neural')}
              className={`quantum-nav-button group ${
                currentPage === 'neural'
                  ? 'quantum-nav-active'
                  : 'quantum-nav-inactive'
              }`}
            >
              <div className="quantum-button-orb">
                <Brain className="w-5 h-5 transition-transform duration-300 group-hover:scale-110" />
              </div>
              <span className="font-semibold tracking-wide">Neural Interface</span>
              {currentPage === 'neural' && <div className="quantum-active-indicator" />}
            </button>
            
            <button
              onClick={() => onPageChange('operations')}
              className={`quantum-nav-button group ${
                currentPage === 'operations'
                  ? 'quantum-nav-active'
                  : 'quantum-nav-inactive'
              }`}
            >
              <div className="quantum-button-orb">
                <Activity className="w-5 h-5 transition-transform duration-300 group-hover:scale-110" />
              </div>
              <span className="font-semibold tracking-wide">Operations Hub</span>
              {currentPage === 'operations' && <div className="quantum-active-indicator" />}
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;