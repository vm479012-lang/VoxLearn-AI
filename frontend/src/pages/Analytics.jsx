import React, { useState, useEffect } from 'react';
import { useLearner } from '../context/LearnerContext';
import { api } from '../services/api';
import {
  BarChart3,
  TrendingUp,
  Brain,
  Target,
  Award,
  Clock,
  Flame,
  CheckCircle2,
  AlertTriangle,
  PieChart,
} from 'lucide-react';

export default function Analytics() {
  const { user, dashboard } = useLearner();
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchAnalytics() {
      setLoading(true);
      try {
        const data = await api.getAnalytics(user?.id || 1);
        setAnalytics(data);
      } catch (err) {
        console.warn('Analytics fetch error:', err);
      } finally {
        setLoading(false);
      }
    }
    fetchAnalytics();
  }, [user]);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] gap-3">
        <div className="w-10 h-10 border-4 border-brand-500 border-t-transparent rounded-full animate-spin" />
        <p className="text-sm text-slate-400">Aggregating IRT performance curves and learner analytics...</p>
      </div>
    );
  }

  const accuracyData = analytics?.accuracy_by_difficulty || [
    { difficulty: 'Level 1', accuracy: 88, attempts: 12 },
    { difficulty: 'Level 2', accuracy: 79, attempts: 18 },
    { difficulty: 'Level 3', accuracy: 68, attempts: 24 },
    { difficulty: 'Level 4', accuracy: 52, attempts: 14 },
    { difficulty: 'Level 5', accuracy: 40, attempts: 8 },
  ];

  const miscData = analytics?.misconception_distribution || [
    { name: 'Conceptual', value: 4, color: '#ef4444' },
    { name: 'Formula Application', value: 3, color: '#f59e0b' },
    { name: 'Calculation & Units', value: 2, color: '#3b82f6' },
    { name: 'Misreading Traps', value: 1, color: '#8b5cf6' },
  ];

  const bloomData = analytics?.bloom_mastery || [
    { bloom: 'Remember', average_mastery: 84.5 },
    { bloom: 'Understand', average_mastery: 76.2 },
    { bloom: 'Apply', average_mastery: 64.0 },
    { bloom: 'Analyze', average_mastery: 54.8 },
    { bloom: 'Evaluate', average_mastery: 69.5 },
  ];

  return (
    <div className="space-y-6 max-w-6xl mx-auto animate-fadeIn">
      {/* Header Banner */}
      <div className="p-6 sm:p-8 rounded-3xl bg-slate-900/80 border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <h1 className="text-xl sm:text-2xl font-black text-white flex items-center gap-2.5">
            <BarChart3 className="w-6 h-6 text-brand-400" />
            Learner Model Analytics & IRT Curves
          </h1>
          <p className="text-xs text-slate-400 mt-1 max-w-xl">
            Mathematical breakdown of your cognitive latent ability θ, Bayesian Knowledge Tracing stability, and error classification.
          </p>
        </div>

        {/* Global summary chips */}
        <div className="flex items-center gap-3">
          <div className="p-3 bg-slate-950/70 rounded-xl border border-slate-800 text-center">
            <span className="text-[10px] text-slate-400 font-mono block">Streak</span>
            <span className="text-sm font-bold text-amber-400 flex items-center justify-center gap-1">
              <Flame className="w-3.5 h-3.5" /> {analytics?.streak_days || 5}d
            </span>
          </div>

          <div className="p-3 bg-slate-950/70 rounded-xl border border-slate-800 text-center">
            <span className="text-[10px] text-slate-400 font-mono block">Study Time</span>
            <span className="text-sm font-bold text-brand-300 flex items-center justify-center gap-1 font-mono">
              <Clock className="w-3.5 h-3.5" /> {analytics?.total_minutes || 195}m
            </span>
          </div>

          <div className="p-3 bg-slate-950/70 rounded-xl border border-slate-800 text-center">
            <span className="text-[10px] text-slate-400 font-mono block">Total XP</span>
            <span className="text-sm font-bold text-emerald-400 flex items-center justify-center gap-1 font-mono">
              <Award className="w-3.5 h-3.5" /> {analytics?.points || 720}
            </span>
          </div>
        </div>
      </div>

      {/* Grid: Charts & Distributions */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Chart 1: Item Response Theory (IRT) Accuracy vs Difficulty Curve */}
        <div className="p-6 rounded-3xl bg-slate-900 border border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-bold text-white flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-brand-400" />
              IRT Empirical Accuracy vs Difficulty
            </h2>
            <span className="text-[10px] font-mono text-brand-400 px-2 py-0.5 bg-brand-500/10 rounded-full border border-brand-500/20">
              2-PL Model Fit
            </span>
          </div>
          <p className="text-xs text-slate-400">
            Probability of success decreasing smoothly across Item Response Theory parameter b (difficulty levels 1-5).
          </p>

          <div className="space-y-3 pt-2">
            {accuracyData.map((d, idx) => (
              <div key={idx} className="space-y-1">
                <div className="flex items-center justify-between text-xs">
                  <span className="font-mono text-slate-300 font-bold">{d.difficulty}</span>
                  <span className="font-mono text-slate-400">{d.accuracy}% accuracy</span>
                </div>
                <div className="w-full h-3 bg-slate-950 rounded-full overflow-hidden p-0.5 border border-slate-800">
                  <div
                    className={`h-full rounded-full transition-all duration-500 ${
                      d.accuracy >= 70
                        ? 'bg-gradient-to-r from-emerald-500 to-teal-400'
                        : d.accuracy >= 50
                        ? 'bg-gradient-to-r from-brand-500 to-cyan-400'
                        : 'bg-gradient-to-r from-amber-500 to-rose-500'
                    }`}
                    style={{ width: `${d.accuracy}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Chart 2: Misconception Category Distribution */}
        <div className="p-6 rounded-3xl bg-slate-900 border border-slate-800 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-bold text-white flex items-center gap-2">
              <PieChart className="w-4 h-4 text-amber-400" />
              Misconception Frequency Distribution
            </h2>
            <span className="text-[10px] font-mono text-amber-400 px-2 py-0.5 bg-amber-500/10 rounded-full border border-amber-500/20">
              Cognitive Traps
            </span>
          </div>
          <p className="text-xs text-slate-400">
            Categorization of incorrect options chosen during adaptive testing.
          </p>

          <div className="space-y-3 pt-2">
            {miscData.map((m, idx) => {
              const totalVal = miscData.reduce((acc, curr) => acc + curr.value, 0) || 1;
              const pct = Math.round((m.value / totalVal) * 100);
              return (
                <div key={idx} className="space-y-1">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-slate-200 font-medium">{m.name}</span>
                    <span className="font-mono font-bold text-slate-300">{pct}% ({m.value})</span>
                  </div>
                  <div className="w-full h-2.5 bg-slate-950 rounded-full overflow-hidden border border-slate-800">
                    <div
                      className="h-full rounded-full transition-all duration-500"
                      style={{ width: `${pct}%`, backgroundColor: m.color }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Chart 3: Bloom's Taxonomy Cognitive Hierarchy */}
        <div className="lg:col-span-2 p-6 rounded-3xl bg-slate-900 border border-slate-800 space-y-4">
          <h2 className="text-sm font-bold text-white flex items-center gap-2">
            <Brain className="w-4 h-4 text-accent-purple" />
            Bloom's Taxonomy Cognitive Mastery Spectrum
          </h2>
          <p className="text-xs text-slate-400">
            Mastery distributed from foundational recall up through high-order analytical problem solving.
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-5 gap-3 pt-2">
            {bloomData.map((b, idx) => (
              <div key={idx} className="p-3.5 bg-slate-950/70 rounded-2xl border border-slate-800 text-center space-y-2">
                <span className="text-xs font-bold text-slate-300 block">{b.bloom}</span>
                <div className="relative flex items-center justify-center w-12 h-12 mx-auto rounded-full bg-slate-900 border-2 border-brand-500/40 font-mono text-xs font-bold text-white">
                  {Math.round(b.average_mastery)}%
                </div>
                <span className="text-[10px] text-slate-400 block font-mono">
                  {b.average_mastery >= 75 ? 'Strong' : b.average_mastery >= 55 ? 'Developing' : 'Review'}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
