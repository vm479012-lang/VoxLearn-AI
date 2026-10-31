import React, { useState } from 'react';
import { useVoice } from '../context/VoiceContext';
import { Mic, Zap, Keyboard, Sparkles, CheckCircle2, X } from 'lucide-react';

export default function WisprFlowModal() {
  const { isWisprModalOpen, setIsWisprModalOpen, wisprFlowActive, setWisprFlowActive, injectWisprDictation } = useVoice();
  const [testInput, setTestInput] = useState('');
  const [copiedNotification, setCopiedNotification] = useState(false);

  if (!isWisprModalOpen) return null;

  const handleApplyTest = () => {
    if (testInput.trim()) {
      injectWisprDictation(testInput.trim());
      setCopiedNotification(true);
      setTimeout(() => {
        setCopiedNotification(false);
        setIsWisprModalOpen(false);
      }, 800);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md animate-fadeIn">
      <div className="relative w-full max-w-xl bg-slate-900 border border-brand-500/30 rounded-2xl p-6 shadow-2xl overflow-hidden">
        {/* Glow accent */}
        <div className="absolute -top-16 -right-16 w-48 h-48 bg-brand-500/20 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute -bottom-16 -left-16 w-48 h-48 bg-accent-purple/20 rounded-full blur-3xl pointer-events-none" />

        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-slate-800">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-brand-500/20 text-brand-400 rounded-xl border border-brand-500/30">
              <Zap className="w-6 h-6 animate-pulse" />
            </div>
            <div>
              <h2 className="text-xl font-bold text-white flex items-center gap-2">
                Wispr Flow Integration
                <span className="text-xs px-2 py-0.5 rounded-full bg-brand-500/20 text-brand-300 border border-brand-500/30">
                  Voice-First
                </span>
              </h2>
              <p className="text-xs text-slate-400">High-speed, voice dictation for STEM learning</p>
            </div>
          </div>
          <button
            onClick={() => setIsWisprModalOpen(false)}
            className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="mt-5 space-y-4 text-sm text-slate-300">
          <div className="p-3.5 bg-slate-800/60 rounded-xl border border-slate-700/60">
            <h3 className="font-semibold text-white flex items-center gap-2 mb-1.5">
              <Sparkles className="w-4 h-4 text-amber-400" />
              How VoxLearn + Wispr Flow Works
            </h3>
            <p className="text-xs text-slate-300 leading-relaxed">
              VoxLearn AI is engineered for voice-first interactions. When using Wispr Flow,
              you can hold your Wispr Flow hotkey from anywhere on your desktop to dictate complex physics formulas,
              ask socratic questions, or answer adaptive quiz items 3x faster than typing.
            </p>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div className="p-3 bg-slate-950/60 border border-slate-800 rounded-xl">
              <div className="flex items-center gap-2 text-xs font-semibold text-slate-200 mb-1">
                <Keyboard className="w-3.5 h-3.5 text-brand-400" />
                Wispr Global Shortcut
              </div>
              <p className="text-xs text-slate-400 font-mono">
                Press and hold <span className="text-brand-300 font-bold">Right Option / Alt</span> or your customized Wispr Flow shortcut.
              </p>
            </div>

            <div className="p-3 bg-slate-950/60 border border-slate-800 rounded-xl">
              <div className="flex items-center gap-2 text-xs font-semibold text-slate-200 mb-1">
                <Mic className="w-3.5 h-3.5 text-emerald-400" />
                Browser Speech Fallback
              </div>
              <p className="text-xs text-slate-400">
                Web Speech API is active automatically if Wispr Flow desktop app is not running.
              </p>
            </div>
          </div>

          {/* Integration Status Toggle */}
          <div className="flex items-center justify-between p-3 bg-slate-800/40 border border-slate-700/50 rounded-xl">
            <div className="text-xs">
              <span className="font-semibold text-white">Wispr Flow Listening Mode</span>
              <p className="text-slate-400">Enables high-fidelity STEM dictionary parser</p>
            </div>
            <button
              onClick={() => setWisprFlowActive(!wisprFlowActive)}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                wisprFlowActive ? 'bg-brand-500' : 'bg-slate-700'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  wisprFlowActive ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>

          {/* Test Playground */}
          <div>
            <label className="block text-xs font-medium text-slate-300 mb-1.5">
              Test Voice Dictation / Direct Text Injection:
            </label>
            <textarea
              value={testInput}
              onChange={(e) => setTestInput(e.target.value)}
              placeholder="Speak with Wispr Flow or type e.g. 'Can you explain why current is conserved in a series circuit?'"
              rows={2}
              className="w-full px-3.5 py-2.5 bg-slate-950 border border-slate-700 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500"
            />
          </div>
        </div>

        {/* Footer */}
        <div className="mt-5 flex items-center justify-between pt-4 border-t border-slate-800">
          <span className="text-xs text-slate-400 flex items-center gap-1.5">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            Wispr Flow Protocol Ready
          </span>
          <div className="flex gap-2">
            <button
              onClick={() => setIsWisprModalOpen(false)}
              className="px-4 py-2 text-xs font-medium text-slate-300 hover:text-white bg-slate-800 hover:bg-slate-700 rounded-xl transition-colors"
            >
              Close
            </button>
            <button
              onClick={handleApplyTest}
              disabled={!testInput.trim()}
              className="px-4 py-2 text-xs font-semibold text-white bg-brand-500 hover:bg-brand-600 disabled:opacity-50 disabled:cursor-not-allowed rounded-xl shadow-lg shadow-brand-500/20 transition-all flex items-center gap-1.5"
            >
              {copiedNotification ? (
                <>
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  Injected!
                </>
              ) : (
                <>
                  <Sparkles className="w-3.5 h-3.5" />
                  Inject into AI Tutor
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
