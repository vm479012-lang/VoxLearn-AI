import React, { useState, useEffect } from 'react';
import { useLearner } from '../context/LearnerContext';
import { api } from '../services/api';
import {
  Network,
  CheckCircle2,
  AlertTriangle,
  Clock,
  ArrowRight,
  BookOpen,
  Filter,
  Search,
  Sparkles,
  Layers,
  ChevronRight,
  X,
} from 'lucide-react';

export default function MasteryView({ onNavigate }) {
  const { user } = useLearner();
  const [concepts, setConcepts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedTopic, setSelectedTopic] = useState('All');
  const [selectedStatus, setSelectedStatus] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');
  const [activeConcept, setActiveConcept] = useState(null);
  const [activeDetail, setActiveDetail] = useState(null);
  const [detailLoading, setDetailLoading] = useState(false);

  useEffect(() => {
    async function loadMastery() {
      setLoading(true);
      try {
        const data = await api.getMasteryOverview(user?.id || 1);
        setConcepts(data);
      } catch (err) {
        console.warn('Mastery overview error:', err);
      } finally {
        setLoading(false);
      }
    }
    loadMastery();
  }, [user]);

  const handleSelectConcept = async (concept) => {
    setActiveConcept(concept);
    setDetailLoading(true);
    try {
      const detail = await api.getConceptDetail(concept.id, user?.id || 1);
      setActiveDetail(detail);
    } catch (err) {
      console.warn('Concept detail load error:', err);
      setActiveDetail(concept);
    } finally {
      setDetailLoading(false);
    }
  };

  const topics = ['All', 'Electricity', 'Light: Reflection & Refraction', 'Magnetic Effects of Electric Current', 'The Human Eye and Colourful World', 'Sources of Energy'];

  const filteredConcepts = concepts.filter(c => {
    const matchesTopic = selectedTopic === 'All' || c.topic === selectedTopic;
    const matchesStatus = selectedStatus === 'All' || c.status === selectedStatus;
    const matchesSearch = c.name.toLowerCase().includes(searchQuery.toLowerCase()) || c.description.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesTopic && matchesStatus && matchesSearch;
  });

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] gap-3">
        <div className="w-10 h-10 border-4 border-brand-500 border-t-transparent rounded-full animate-spin" />
        <p className="text-sm text-slate-400">Loading Class 10 Physics Knowledge Graph...</p>
      </div>
    );
  }

  return (
    <div className="space-y-6 max-w-6xl mx-auto animate-fadeIn">
      {/* Header Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-6 bg-slate-900/80 rounded-3xl border border-slate-800">
        <div>
          <h1 className="text-xl sm:text-2xl font-black text-white flex items-center gap-2.5">
            <Network className="w-6 h-6 text-brand-400" />
            Class 10 Physics Concept Mastery Graph
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Bayesian Knowledge Tracing tracks your latent mastery probability across 17 syllabus nodes.
          </p>
        </div>

        {/* Global Stats Summary */}
        <div className="flex items-center gap-2">
          <div className="px-3 py-1.5 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-xs font-mono font-semibold">
            {concepts.filter(c => c.status === 'mastered').length} Mastered
          </div>
          <div className="px-3 py-1.5 rounded-xl bg-brand-500/10 border border-brand-500/20 text-brand-300 text-xs font-mono font-semibold">
            {concepts.filter(c => c.status === 'in_progress').length} In Progress
          </div>
          <div className="px-3 py-1.5 rounded-xl bg-rose-500/10 border border-rose-500/20 text-rose-300 text-xs font-mono font-semibold">
            {concepts.filter(c => c.status === 'needs_review').length} Review
          </div>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3 p-3 bg-slate-900/60 rounded-2xl border border-slate-800/80">
        {/* Search */}
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-3" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search concepts, formulas, or Bloom's levels..."
            className="w-full pl-10 pr-4 py-2 bg-slate-950 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:border-brand-500"
          />
        </div>

        {/* Topic filter buttons */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 md:pb-0 no-scrollbar">
          {topics.map((t) => (
            <button
              key={t}
              onClick={() => setSelectedTopic(t)}
              className={`px-3 py-1.5 rounded-xl text-xs font-medium whitespace-nowrap transition-all ${
                selectedTopic === t
                  ? 'bg-brand-500 text-white shadow-md'
                  : 'bg-slate-950 text-slate-400 hover:text-white border border-slate-800'
              }`}
            >
              {t}
            </button>
          ))}
        </div>
      </div>

      {/* Main Grid: Concepts List & Active Detail Drawer */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Cols: Concept Nodes List */}
        <div className="lg:col-span-2 space-y-3">
          {filteredConcepts.map((c) => {
            const isSelected = activeConcept?.id === c.id;
            return (
              <div
                key={c.id}
                onClick={() => handleSelectConcept(c)}
                className={`cursor-pointer p-4 rounded-2xl border transition-all ${
                  isSelected
                    ? 'bg-slate-900 border-brand-500 shadow-lg shadow-brand-500/10'
                    : 'bg-slate-900/70 hover:bg-slate-900 border-slate-800 hover:border-slate-700'
                }`}
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="text-[10px] px-2 py-0.5 rounded-md font-mono bg-slate-800 text-slate-300 border border-slate-700">
                        {c.topic}
                      </span>
                      <span className="text-[10px] text-slate-500 font-mono">
                        Bloom: {c.bloom_level}
                      </span>
                    </div>
                    <h3 className="text-sm font-bold text-white">{c.name}</h3>
                    <p className="text-xs text-slate-400 line-clamp-1">{c.description}</p>
                  </div>

                  <div className="text-right shrink-0">
                    <div className="flex items-center justify-end gap-1.5">
                      <span
                        className={`text-xs font-bold font-mono ${
                          c.mastery_percentage >= 80
                            ? 'text-emerald-400'
                            : c.mastery_percentage >= 50
                            ? 'text-brand-300'
                            : 'text-rose-400'
                        }`}
                      >
                        {c.mastery_percentage}%
                      </span>
                      <ChevronRight className="w-4 h-4 text-slate-500" />
                    </div>
                    <span
                      className={`text-[9px] uppercase font-mono px-2 py-0.5 rounded-full inline-block mt-1 ${
                        c.status === 'mastered'
                          ? 'bg-emerald-500/20 text-emerald-300'
                          : c.status === 'in_progress'
                          ? 'bg-brand-500/20 text-brand-300'
                          : 'bg-rose-500/20 text-rose-300'
                      }`}
                    >
                      {c.status.replace('_', ' ')}
                    </span>
                  </div>
                </div>

                {/* Progress Mini Bar */}
                <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden mt-3">
                  <div
                    className={`h-full rounded-full transition-all duration-300 ${
                      c.mastery_percentage >= 80
                        ? 'bg-emerald-400'
                        : c.mastery_percentage >= 50
                        ? 'bg-brand-500'
                        : 'bg-rose-500'
                    }`}
                    style={{ width: `${c.mastery_percentage}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>

        {/* Right Col: Concept Deep-Dive Drawer */}
        <div className="space-y-4">
          {activeConcept ? (
            <div className="p-6 rounded-3xl bg-slate-900 border border-slate-800 space-y-5 sticky top-20 shadow-xl">
              <div className="flex items-center justify-between pb-3 border-b border-slate-800">
                <span className="text-[10px] uppercase font-mono font-bold text-brand-400">
                  Concept Deep-Dive
                </span>
                <button
                  onClick={() => setActiveConcept(null)}
                  className="p-1 text-slate-400 hover:text-white rounded-lg"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>

              <div>
                <span className="text-xs text-slate-400 font-mono">{activeConcept.topic}</span>
                <h2 className="text-base font-bold text-white mt-0.5">{activeConcept.name}</h2>
                <p className="text-xs text-slate-300 mt-2 leading-relaxed">{activeConcept.description}</p>
              </div>

              {/* Real World Analogy */}
              {activeConcept.real_world_analogy && (
                <div className="p-3 bg-slate-950/70 rounded-xl border border-slate-800">
                  <span className="text-[10px] font-bold text-amber-400 uppercase font-mono block mb-1">
                    💡 Mental Model / Analogy:
                  </span>
                  <p className="text-xs text-slate-300 italic">{activeConcept.real_world_analogy}</p>
                </div>
              )}

              {/* Formulas */}
              {activeConcept.formulas && activeConcept.formulas.length > 0 && (
                <div className="space-y-1.5">
                  <span className="text-[10px] font-bold text-slate-400 uppercase font-mono block">
                    Governing Equations:
                  </span>
                  <div className="space-y-1">
                    {activeConcept.formulas.map((f, idx) => (
                      <div key={idx} className="p-2 bg-slate-950 rounded-lg text-xs font-mono text-brand-300 border border-slate-800">
                        {f}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Prerequisite Check */}
              {activeDetail?.prerequisite_check && (
                <div className="p-3 bg-slate-950/70 rounded-xl border border-slate-800 text-xs">
                  <span className="text-[10px] font-bold text-slate-400 uppercase font-mono block mb-1">
                    Prerequisite Knowledge Status:
                  </span>
                  <div className="flex items-center gap-2">
                    {activeDetail.prerequisite_check.is_ready ? (
                      <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                    ) : (
                      <AlertTriangle className="w-4 h-4 text-amber-400" />
                    )}
                    <span className={activeDetail.prerequisite_check.is_ready ? "text-emerald-300 font-semibold" : "text-amber-300 font-semibold"}>
                      {activeDetail.prerequisite_check.recommendation}
                    </span>
                  </div>
                </div>
              )}

              <button
                onClick={() => onNavigate('quiz')}
                className="w-full py-2.5 rounded-xl bg-brand-500 hover:bg-brand-600 text-white font-bold text-xs shadow-lg shadow-brand-500/25 transition-all flex items-center justify-center gap-2"
              >
                <span>Launch Adaptive Quiz on this Concept</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          ) : (
            <div className="p-6 rounded-3xl bg-slate-900/50 border border-slate-800/80 text-center space-y-3 py-12">
              <BookOpen className="w-8 h-8 text-slate-600 mx-auto" />
              <p className="text-xs text-slate-400 max-w-xs mx-auto">
                Select any concept node on the left to inspect its Bayesian Knowledge Tracing parameters, governing equations, and prerequisite dependencies.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
