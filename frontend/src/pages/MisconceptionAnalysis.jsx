import React, { useState, useEffect } from 'react';
import { useLearner } from '../context/LearnerContext';
import { api } from '../services/api';
import {
  AlertTriangle,
  Lightbulb,
  CheckCircle2,
  XCircle,
  HelpCircle,
  Filter,
  Brain,
  ArrowRight,
  ShieldAlert,
} from 'lucide-react';

export default function MisconceptionAnalysis({ onNavigate }) {
  const { user } = useLearner();
  const [misconceptions, setMisconceptions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [expandedId, setExpandedId] = useState(null);

  useEffect(() => {
    async function fetchMisconceptions() {
      setLoading(true);
      try {
        const data = await api.getMisconceptions(user?.id || 1);
        setMisconceptions(data);
        if (data.length > 0) setExpandedId(data[0].id);
      } catch (err) {
        console.warn('Misconceptions load fallback:', err);
      } finally {
        setLoading(false);
      }
    }
    fetchMisconceptions();
  }, [user]);

  const categories = ['All', 'conceptual', 'formula_application', 'calculation_unit', 'misreading'];

  const filtered = misconceptions.filter(m => {
    return selectedCategory === 'All' || m.category === selectedCategory;
  });

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] gap-3">
        <div className="w-10 h-10 border-4 border-brand-500 border-t-transparent rounded-full animate-spin" />
        <p className="text-sm text-slate-400">Loading Wrong-Answer Reasoning Diagnostic Bank...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-5xl mx-auto animate-fadeIn">
      {/* Header */}
      <div className="p-6 sm:p-8 rounded-3xl bg-slate-900/80 border border-slate-800 space-y-2">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-amber-500/10 border border-amber-500/20 text-xs font-semibold text-amber-300">
          <ShieldAlert className="w-3.5 h-3.5" />
          <span>Cognitive Diagnostic Engine</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-black text-white">Wrong-Answer Reasoning Analysis</h1>
        <p className="text-xs sm:text-sm text-slate-400 max-w-2xl leading-relaxed">
          Standard quizzes only tell you <span className="text-slate-200 font-semibold">if</span> an answer is wrong.
          VoxLearn AI diagnoses <span className="text-brand-300 font-semibold">why</span> your reasoning failed—differentiating between
          conceptual misunderstandings, sign conventions, and calculation slips.
        </p>
      </div>

      {/* Category Tabs */}
      <div className="flex items-center gap-2 overflow-x-auto pb-1 no-scrollbar">
        {categories.map((cat) => (
          <button
            key={cat}
            onClick={() => setSelectedCategory(cat)}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-semibold whitespace-nowrap transition-all capitalize ${
              selectedCategory === cat
                ? 'bg-brand-500 text-white shadow-md'
                : 'bg-slate-900 text-slate-400 hover:text-white border border-slate-800'
            }`}
          >
            {cat.replace('_', ' ')}
          </button>
        ))}
      </div>

      {/* Misconceptions Accordion Cards */}
      <div className="space-y-4">
        {filtered.map((misc) => {
          const isExpanded = expandedId === misc.id;
          return (
            <div
              key={misc.id}
              className={`rounded-2xl border transition-all overflow-hidden ${
                isExpanded
                  ? 'bg-slate-900 border-brand-500/40 shadow-xl'
                  : 'bg-slate-900/60 hover:bg-slate-900 border-slate-800'
              }`}
            >
              <div
                onClick={() => setExpandedId(isExpanded ? null : misc.id)}
                className="cursor-pointer p-5 flex items-center justify-between gap-4"
              >
                <div className="flex items-center gap-3">
                  <div className="p-2.5 rounded-xl bg-amber-500/10 text-amber-400 shrink-0">
                    <AlertTriangle className="w-5 h-5" />
                  </div>
                  <div>
                    <div className="flex items-center gap-2">
                      <h3 className="text-sm sm:text-base font-bold text-white">{misc.title}</h3>
                      <span className="text-[10px] px-2 py-0.5 rounded-full font-mono bg-slate-800 text-slate-300 border border-slate-700 capitalize">
                        {misc.category.replace('_', ' ')}
                      </span>
                    </div>
                    <p className="text-xs text-slate-400 mt-0.5">{misc.description}</p>
                  </div>
                </div>

                <div className="text-right shrink-0">
                  <span className="text-[10px] text-brand-400 font-mono font-bold block">
                    {misc.concept_name}
                  </span>
                </div>
              </div>

              {isExpanded && (
                <div className="px-5 pb-5 pt-2 border-t border-slate-800/80 space-y-4 text-xs text-slate-300 leading-relaxed animate-fadeIn">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2">
                    <div className="p-3.5 bg-slate-950/80 rounded-xl border border-slate-800 space-y-1">
                      <span className="text-[10px] font-bold text-rose-400 uppercase font-mono block">
                        Why Learners Fall for This:
                      </span>
                      <p>{misc.why_it_happens}</p>
                    </div>

                    <div className="p-3.5 bg-slate-950/80 rounded-xl border border-slate-800 space-y-1">
                      <span className="text-[10px] font-bold text-emerald-400 uppercase font-mono block">
                        Physical Reality:
                      </span>
                      <p>{misc.physical_reality}</p>
                    </div>
                  </div>

                  <div className="p-3.5 bg-brand-950/40 rounded-xl border border-brand-500/30 flex items-start gap-2.5 text-brand-200">
                    <Lightbulb className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
                    <div>
                      <strong className="text-white block mb-0.5">Micro-Remedy & Mental Model:</strong>
                      <p>{misc.remedy_tip}</p>
                    </div>
                  </div>

                  <button
                    onClick={() => onNavigate('practice')}
                    className="py-2 px-4 rounded-xl bg-brand-500/20 hover:bg-brand-500/30 text-brand-300 border border-brand-500/40 text-xs font-semibold transition-all flex items-center gap-1.5"
                  >
                    <span>Practice Micro-Remedy Challenge</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
