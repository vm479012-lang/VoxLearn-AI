import React from 'react';
import { useLearner } from '../context/LearnerContext';
import { useVoice } from '../context/VoiceContext';
import { Flame, Award, Mic, Zap, User, Sparkles } from 'lucide-react';
import AudioVisualizer from './AudioVisualizer';

export default function Navbar({ onNavigate, currentPage }) {
  const { user } = useLearner();
  const { isListening, isSpeaking, audioLevel, wisprFlowActive, setIsWisprModalOpen } = useVoice();

  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-800 bg-slate-950/80 backdrop-blur-xl">
      <div className="flex items-center justify-between h-16 px-4 md:px-8 max-w-7xl mx-auto">
        {/* Brand & Tagline */}
        <div className="flex items-center gap-3 cursor-pointer" onClick={() => onNavigate('dashboard')}>
          <div className="relative flex items-center justify-center w-10 h-10 rounded-xl bg-gradient-to-br from-brand-500 to-accent-violet shadow-lg shadow-brand-500/25">
            <Mic className="w-5 h-5 text-white animate-pulse" />
            <div className="absolute -inset-1 rounded-xl bg-brand-400/20 blur-sm -z-10" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-lg font-black tracking-tight text-white">VoxLearn</span>
              <span className="text-xs px-1.5 py-0.5 rounded-md font-mono font-bold bg-brand-500/20 text-brand-300 border border-brand-500/30">
                AI
              </span>
            </div>
            <p className="text-[10px] text-slate-400 font-medium hidden sm:block">
              AI Prep Tutor with Learner Model • Class 10 Physics
            </p>
          </div>
        </div>

        {/* Center: Live Voice / Wispr Status Indicator */}
        <div className="hidden lg:flex items-center gap-3">
          <AudioVisualizer isActive={isListening} isSpeaking={isSpeaking} level={audioLevel} />

          {/* Wispr Flow Action Pill */}
          <button
            onClick={() => setIsWisprModalOpen(true)}
            className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-900 border border-slate-700 hover:border-brand-500/50 transition-all text-xs text-slate-300 hover:text-white"
            title="Configure Wispr Flow voice dictation"
          >
            <div className={`w-2 h-2 rounded-full ${wisprFlowActive ? 'bg-emerald-400 shadow-[0_0_8px_#34d399]' : 'bg-slate-500'}`} />
            <Zap className="w-3.5 h-3.5 text-amber-400" />
            <span className="font-medium">Wispr Flow Ready</span>
          </button>
        </div>

        {/* Right Stats & Profile */}
        <div className="flex items-center gap-2 sm:gap-3">
          {/* Streak */}
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-300 text-xs font-semibold">
            <Flame className="w-4 h-4 text-amber-400 animate-bounce" />
            <span>{user?.streak_days || 5}d Streak</span>
          </div>

          {/* Points */}
          <div className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-brand-500/10 border border-brand-500/20 text-brand-300 text-xs font-semibold">
            <Award className="w-4 h-4 text-brand-400" />
            <span>{user?.points || 720} XP</span>
          </div>

          {/* Onboarding / Profile Button */}
          <button
            onClick={() => onNavigate('onboarding')}
            className={`flex items-center gap-2 p-1.5 sm:px-3 sm:py-1.5 rounded-xl border transition-all text-xs font-medium ${
              currentPage === 'onboarding'
                ? 'bg-brand-500 text-white border-brand-400'
                : 'bg-slate-900 text-slate-300 border-slate-800 hover:border-slate-700'
            }`}
          >
            <User className="w-4 h-4 text-brand-400" />
            <span className="hidden sm:inline">{user?.name ? user.name.split(' ')[0] : 'Profile'}</span>
          </button>
        </div>
      </div>
    </header>
  );
}
