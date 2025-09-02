import React, { useState } from 'react';
import NeuralCenter from './components/NeuralCenter';
import OperationsDashboard from './components/OperationsDashboard';
import Navigation from './components/Navigation';
import './styles/quantum-animations.css';

function App() {
  const [currentPage, setCurrentPage] = useState<'neural' | 'operations'>('neural');

  return (
    <div className="min-h-screen bg-black relative overflow-hidden">
      {/* Quantum Field Background */}
      <div className="absolute inset-0 quantum-field" />
      <div className="absolute inset-0 neural-pathways opacity-20" />
      
      {/* Floating Quantum Particles */}
      <div className="absolute inset-0 quantum-particles" />
      
      {/* Holographic Overlay */}
      <div className="absolute inset-0 holographic-overlay opacity-10" />
      
      <Navigation currentPage={currentPage} onPageChange={setCurrentPage} />
      
      <main className="relative z-10 min-h-screen pt-24">
        <div className={`transition-all duration-1000 ease-out ${
          currentPage === 'neural' 
            ? 'opacity-100 transform translate-x-0 scale-100' 
            : 'opacity-0 transform translate-x-full scale-95 pointer-events-none'
        }`}>
          {currentPage === 'neural' && <NeuralCenter />}
        </div>
        
        <div className={`transition-all duration-1000 ease-out ${
          currentPage === 'operations' 
            ? 'opacity-100 transform translate-x-0 scale-100' 
            : 'opacity-0 transform -translate-x-full scale-95 pointer-events-none'
        }`}>
          {currentPage === 'operations' && <OperationsDashboard />}
        </div>
      </main>
    </div>
  );
}

export default App;