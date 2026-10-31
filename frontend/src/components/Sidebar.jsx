import React from 'react';
import {
  LayoutDashboard,
  Bot,
  BrainCircuit,
  Network,
  AlertTriangle,
  Dumbbell,
  BarChart3,
  HelpCircle,
  Zap,
} from 'lucide-react';
import { useVoice } from '../context/VoiceContext';

export default function Sidebar({ currentPage, onNavigate }) {
  const { setIsWisprModalOpen } = useVoice();

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard, badge: null },
    { id: 'tutor', label: 'AI Socratic Tutor', icon: Bot, badge: 'Voice' },
    { id: 'quiz', label: 'Adaptive Quiz', icon: BrainCircuit, badge: 'BKT' },
    { id: 'mastery', label: 'Concept Mastery', icon: Network, badge: null },
    { id: 'misconceptions', label: 'Wrong-Answer Insights', icon: AlertTriangle, badge: 'Reasoning' },
    { id: 'practice', label: 'Personalized Practice', icon: Dumbbell, badge: 'Targeted' },
    { id: 'analytics', label: 'Progress & IRT', icon: BarChart3, badge: null },
  ];

  return (
    <aside className="w-64 border-r border-slate-800 bg-slate-950/70 p-4 flex flex-col justify-between shrink-0 hidden md:flex">
      <div className="space-y-6">
        {/* Navigation Section */}
        <div>
          <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500 px-3">
            Core Learning Modules
          </span>
          <nav className="mt-3 space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = currentPage === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => onNavigate(item.id)}
                  className={`w-full flex items-center justify-between px-3 py-2.5 rounded-xl text-xs font-semibold transition-all ${
                    isActive
                      ? 'bg-brand-500 text-white shadow-lg shadow-brand-500/25 glow-brand'
                      : 'text-slate-300 hover:text-white hover:bg-slate-900 border border-transparent hover:border-slate-800'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                    <span>{item.label}</span>
                  </div>
                  {item.badge && (
                    <span
                      className={`text-[10px] px-1.5 py-0.5 rounded-md font-mono ${
                        isActive
                          ? 'bg-white/20 text-white'
                          : 'bg-slate-800 text-slate-400 border border-slate-700/60'
                      }`}
                    >
                      {item.badge}
                    </span>
                  )}
                </button>
              );
            })}
          </nav>
        </div>

        {/* Wispr Flow Callout Box */}
        <div className="p-3.5 rounded-2xl bg-gradient-to-br from-slate-900 to-slate-900/40 border border-brand-500/20 relative overflow-hidden">
          <div className="absolute top-0 right-0 p-2">
            <Zap className="w-4 h-4 text-amber-400" />
          </div>
          <div className="flex items-center gap-2 mb-1.5">
            <span className="text-xs font-bold text-white">Wispr Flow Voice</span>
            <span className="text-[9px] px-1.5 py-0.2 bg-emerald-500/20 text-emerald-300 rounded-full font-mono">
              Ready
            </span>
          </div>
          <p className="text-[11px] text-slate-400 mb-2.5 leading-relaxed">
            Dictate physics questions 3x faster with real-time STEM terminology matching.
          </p>
          <button
            onClick={() => setIsWisprModalOpen(true)}
            className="w-full py-1.5 px-3 rounded-lg bg-brand-500/20 hover:bg-brand-500/30 text-brand-300 border border-brand-500/30 text-[11px] font-semibold transition-colors flex items-center justify-center gap-1.5"
          >
            <Zap className="w-3 h-3 text-amber-400" />
            Wispr Shortcut Guide
          </button>
        </div>
      </div>

      {/* Footer Info */}
      <div className="pt-4 border-t border-slate-800 text-[11px] text-slate-500">
        <div className="flex items-center justify-between">
          <span>Hackathon Problem 2</span>
          <span className="text-brand-400 font-mono">v1.0.0</span>
        </div>
        <p className="mt-1 text-[10px] text-slate-400">Class 10 CBSE / NTSE Curriculum</p>
      </div>
    </aside>
  );
}
