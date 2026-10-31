import React from 'react';

export default function AudioVisualizer({ isActive, isSpeaking, level = 50 }) {
  const bars = [14, 28, 45, 75, 95, 60, 85, 40, 20];

  return (
    <div className="flex items-center justify-center gap-1.5 h-10 px-4 py-1.5 bg-slate-900/80 border border-slate-700/60 rounded-full backdrop-blur-md">
      <div className={`w-2.5 h-2.5 rounded-full ${isActive ? 'bg-red-500 animate-ping' : isSpeaking ? 'bg-brand-400 animate-pulse' : 'bg-slate-500'}`} />
      
      <span className="text-xs font-mono font-medium text-slate-300 mr-2">
        {isActive ? 'Listening...' : isSpeaking ? 'AI Speaking' : 'Mic Ready'}
      </span>

      <div className="flex items-center gap-1 h-6">
        {bars.map((defaultHeight, idx) => {
          const dynamicHeight = (isActive || isSpeaking)
            ? Math.max(6, Math.min(28, (defaultHeight * (level / 50))))
            : 6;

          return (
            <div
              key={idx}
              className={`w-1 rounded-full transition-all duration-100 ${
                isActive
                  ? 'bg-gradient-to-t from-red-500 to-amber-400'
                  : isSpeaking
                  ? 'bg-gradient-to-t from-brand-500 to-brand-300'
                  : 'bg-slate-700'
              }`}
              style={{ height: `${dynamicHeight}px` }}
            />
          );
        })}
      </div>
    </div>
  );
}
