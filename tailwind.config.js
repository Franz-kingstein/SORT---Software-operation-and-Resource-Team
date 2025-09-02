/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Rajdhani', 'sans-serif'],
        display: ['Orbitron', 'monospace'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      colors: {
        quantum: {
          blue: '#00D4FF',
          cyan: '#00FFFF', 
          purple: '#8B5CF6',
          pink: '#EC4899',
          green: '#10B981',
          emerald: '#059669',
          yellow: '#F59E0B',
          orange: '#EA580C',
          red: '#EF4444',
        },
        neural: {
          50: '#f0fdff',
          100: '#ccfbff',
          200: '#99f6ff',
          300: '#4ae8ff',
          400: '#00d4ff',
          500: '#00b8e6',
          600: '#0093bf',
          700: '#09759a',
          800: '#10607e',
          900: '#13516b',
        }
      },
      animation: {
        'quantum-spin': 'quantum-spin 1s linear infinite',
        'quantum-pulse': 'quantum-pulse 2s ease-in-out infinite',
        'quantum-ping': 'quantum-ping 2s ease-in-out infinite',
        'quantum-float': 'quantum-float 3s ease-in-out infinite',
        'quantum-glow': 'quantum-glow 2s ease-in-out infinite alternate',
        'quantum-shimmer': 'quantum-shimmer 3s ease-in-out infinite',
        'neural-flow': 'neural-flow 25s linear infinite',
        'quantum-drift': 'quantum-drift 30s ease-in-out infinite',
        'holographic-flow': 'holographic-flow 8s ease-in-out infinite',
      },
      keyframes: {
        'quantum-float': {
          '0%, 100%': { transform: 'translateY(0px) rotateZ(0deg)' },
          '50%': { transform: 'translateY(-10px) rotateZ(5deg)' },
        },
        'quantum-glow': {
          '0%': { 
            boxShadow: '0 0 5px rgba(0, 212, 255, 0.3), 0 0 10px rgba(0, 212, 255, 0.2)' 
          },
          '100%': { 
            boxShadow: '0 0 20px rgba(0, 212, 255, 0.6), 0 0 40px rgba(0, 212, 255, 0.4)' 
          },
        },
        'quantum-shimmer': {
          '0%, 100%': { transform: 'translateX(-100%)' },
          '50%': { transform: 'translateX(100%)' },
        },
        'neural-flow': {
          '0%': { transform: 'translate(0, 0)' },
          '100%': { transform: 'translate(100px, 100px)' },
        },
        'quantum-drift': {
          '0%, 100%': { transform: 'translate(0, 0) rotate(0deg)' },
          '25%': { transform: 'translate(50px, -25px) rotate(90deg)' },
          '50%': { transform: 'translate(0, -50px) rotate(180deg)' },
          '75%': { transform: 'translate(-50px, -25px) rotate(270deg)' },
        },
        'holographic-flow': {
          '0%, 100%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
        },
      },
      backdropBlur: {
        xs: '2px',
        '4xl': '72px',
      },
      perspective: {
        1000: '1000px',
        1500: '1500px',
        2000: '2000px',
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem',
      },
      borderRadius: {
        '4xl': '2rem',
        '5xl': '2.5rem',
      },
      boxShadow: {
        'quantum': '0 0 20px rgba(0, 212, 255, 0.3), 0 0 40px rgba(139, 92, 246, 0.2)',
        'quantum-lg': '0 0 30px rgba(0, 212, 255, 0.4), 0 0 60px rgba(139, 92, 246, 0.3)',
        'neural': '0 8px 32px rgba(0, 212, 255, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.1)',
      },
    },
  },
  plugins: [
    function({ addUtilities }) {
      const newUtilities = {
        '.perspective-1000': {
          perspective: '1000px',
        },
        '.preserve-3d': {
          transformStyle: 'preserve-3d',
        },
        '.backface-hidden': {
          backfaceVisibility: 'hidden',
        },
        '.quantum-text-shadow': {
          textShadow: '0 0 10px currentColor, 0 0 20px currentColor, 0 0 30px currentColor',
        },
      }
      addUtilities(newUtilities)
    }
  ],
};