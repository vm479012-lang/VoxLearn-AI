import React, { useState, useEffect } from 'react';
import { useLearner } from '../context/LearnerContext';
import { api } from '../services/api';
import {
  Dumbbell,
  Sparkles,
  Target,
  CheckCircle2,
  XCircle,
  HelpCircle,
  Lightbulb,
  ArrowRight,
  TrendingUp,
  RotateCcw,
} from 'lucide-react';

export default function PersonalizedPractice({ onNavigate }) {
  const { user, addPoints, refreshDashboard } = useLearner();
  const [workout, setWorkout] = useState(null);
  const [loading, setLoading] = useState(true);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedOpt, setSelectedOpt] = useState(null);
  const [evaluated, setEvaluated] = useState(null);
  const [showAnalogy, setShowAnalogy] = useState(false);
  const [showFormula, setShowFormula] = useState(false);
  const [workoutComplete, setWorkoutComplete] = useState(false);
  const [correctCount, setCorrectCount] = useState(0);

  const loadWorkout = async () => {
    setLoading(true);
    setEvaluated(null);
    setSelectedOpt(null);
    setCurrentIndex(0);
    setWorkoutComplete(false);
    setCorrectCount(0);
    try {
      const data = await api.getWeakWorkout(user?.id || 1);
      setWorkout(data);
    } catch (err) {
      console.warn('Personalized practice workout error:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadWorkout();
  }, [user]);

  const currentQ = workout?.questions?.[currentIndex];

  const handleSubmit = async () => {
    if (selectedOpt === null || !currentQ) return;
    try {
      const res = await api.submitQuizAnswer({
        user_id: user?.id || 1,
        question_id: currentQ.question_id,
        selected_option_index: selectedOpt,
        confidence_level: 4,
        time_taken_seconds: 20
      });
      setEvaluated(res);
      if (res.is_correct) {
        setCorrectCount(prev => prev + 1);
        addPoints(25);
      }
    } catch (err) {
      console.error('Practice submit error:', err);
    }
  };

  const handleNext = () => {
    if (currentIndex + 1 < (workout?.questions?.length || 0)) {
      setCurrentIndex(prev => prev + 1);
      setSelectedOpt(null);
      setEvaluated(null);
      setShowAnalogy(false);
      setShowFormula(false);
    } else {
      setWorkoutComplete(true);
      refreshDashboard();
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] gap-3">
        <div className="w-10 h-10 border-4 border-brand-500 border-t-transparent rounded-full animate-spin" />
        <p className="text-sm text-slate-400">Synthesizing personalized weak-concept workout...</p>
      </div>
    );
  }

  if (workoutComplete) {
    return (
      <div className="max-w-xl mx-auto py-8 text-center space-y-6 animate-fadeIn">
        <div className="p-8 bg-slate-900 rounded-3xl border border-emerald-500/30 shadow-2xl space-y-5">
          <div className="w-16 h-16 mx-auto rounded-2xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center shadow-lg">
            <CheckCircle2 className="w-8 h-8" />
          </div>

          <div className="space-y-1">
            <h1 className="text-2xl font-black text-white">Targeted Workout Complete!</h1>
            <p className="text-xs text-slate-300">
              You reinforced your weakest concepts and elevated your Bayesian mastery state.
            </p>
          </div>

          <div className="p-4 bg-slate-950 rounded-2xl border border-slate-800 flex items-center justify-around text-xs">
            <div>
              <span className="text-[10px] text-slate-400 block font-mono">Accuracy</span>
              <span className="text-base font-bold text-emerald-400 font-mono">
                {Math.round((correctCount / (workout?.questions?.length || 1)) * 100)}%
              </span>
            </div>
            <div>
              <span className="text-[10px] text-slate-400 block font-mono">XP Earned</span>
              <span className="text-base font-bold text-amber-400 font-mono">
                +{correctCount * 25} XP
              </span>
            </div>
          </div>

          <div className="pt-3 flex gap-3 justify-center">
            <button
              onClick={loadWorkout}
              className="py-2.5 px-5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-semibold text-xs"
            >
              Start Another Set
            </button>
            <button
              onClick={() => onNavigate('dashboard')}
              className="py-2.5 px-6 rounded-xl bg-brand-500 hover:bg-brand-600 text-white font-bold text-xs shadow-lg shadow-brand-500/25"
            >
              Return to Dashboard
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!currentQ) return null;

  return (
    <div className="max-w-3xl mx-auto py-4 space-y-6 animate-fadeIn">
      {/* Header */}
      <div className="p-4 bg-slate-900/80 rounded-2xl border border-slate-800 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-amber-500/20 text-amber-400 rounded-xl">
            <Dumbbell className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold text-white">
                Weak Concept Workout ({currentIndex + 1}/{workout?.questions?.length})
              </span>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-slate-800 text-amber-300 font-mono">
                {currentQ.concept_name}
              </span>
            </div>
            <p className="text-[10px] text-slate-400 mt-0.5">Focusing on your lowest-confidence knowledge nodes</p>
          </div>
        </div>
      </div>

      {/* Card */}
      <div className="p-6 sm:p-8 bg-slate-900/90 rounded-3xl border border-slate-800 shadow-xl space-y-6">
        <h2 className="text-base sm:text-lg font-bold text-white leading-relaxed">
          {currentQ.question_text}
        </h2>

        {/* Guided Scaffolding */}
        <div className="flex items-center gap-3">
          {currentQ.formula_hint && (
            <button
              onClick={() => setShowFormula(!showFormula)}
              className="text-xs font-semibold text-brand-400 hover:text-brand-300 flex items-center gap-1.5"
            >
              <Lightbulb className="w-3.5 h-3.5 text-amber-400" />
              <span>{showFormula ? "Hide Formula" : "Formula Scaffolding"}</span>
            </button>
          )}

          {currentQ.analogy && (
            <button
              onClick={() => setShowAnalogy(!showAnalogy)}
              className="text-xs font-semibold text-accent-purple hover:text-purple-300 flex items-center gap-1.5"
            >
              <Sparkles className="w-3.5 h-3.5 text-accent-purple" />
              <span>{showAnalogy ? "Hide Analogy" : "Mental Model Analogy"}</span>
            </button>
          )}
        </div>

        {showFormula && currentQ.formula_hint && (
          <div className="p-3 bg-brand-950/40 border border-brand-500/30 rounded-xl text-xs font-mono text-brand-300 animate-fadeIn">
            {currentQ.formula_hint}
          </div>
        )}

        {showAnalogy && currentQ.analogy && (
          <div className="p-3 bg-purple-950/40 border border-accent-purple/30 rounded-xl text-xs text-purple-200 italic animate-fadeIn">
            💡 {currentQ.analogy}
          </div>
        )}

        {/* Options */}
        <div className="space-y-3">
          {currentQ.options.map((opt, idx) => {
            const isSelected = selectedOpt === idx;
            const isEvaluated = evaluated !== null;
            const isCorrect = isEvaluated && evaluated.correct_option_index === idx;
            const isWrongSelected = isEvaluated && isSelected && !evaluated.is_correct;

            let style = 'bg-slate-950/80 border-slate-800 hover:border-slate-700 text-slate-200';
            if (isEvaluated) {
              if (isCorrect) style = 'border-emerald-500 bg-emerald-950/30 text-emerald-200 font-bold';
              else if (isWrongSelected) style = 'border-rose-500 bg-rose-950/30 text-rose-200';
              else style = 'opacity-50 border-slate-800';
            } else if (isSelected) {
              style = 'border-brand-500 bg-brand-500/10 text-white font-bold';
            }

            return (
              <button
                key={idx}
                onClick={() => !isEvaluated && setSelectedOpt(idx)}
                disabled={isEvaluated}
                className={`w-full p-4 rounded-2xl border text-left text-xs sm:text-sm transition-all flex items-center justify-between ${style}`}
              >
                <span>{opt}</span>
                {isEvaluated && isCorrect && <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />}
                {isEvaluated && isWrongSelected && <XCircle className="w-4 h-4 text-rose-400 shrink-0" />}
              </button>
            );
          })}
        </div>

        {/* Action Button */}
        {!evaluated ? (
          <button
            onClick={handleSubmit}
            disabled={selectedOpt === null}
            className="w-full py-3.5 rounded-xl bg-brand-500 hover:bg-brand-600 disabled:opacity-40 disabled:cursor-not-allowed text-white font-bold text-xs sm:text-sm shadow-lg shadow-brand-500/25 transition-all"
          >
            Check Solution & Update Mastery
          </button>
        ) : (
          <button
            onClick={handleNext}
            className="w-full py-3.5 rounded-xl bg-brand-500 hover:bg-brand-600 text-white font-bold text-xs sm:text-sm shadow-lg shadow-brand-500/25 transition-all flex items-center justify-center gap-2"
          >
            <span>Continue Next Weak Concept</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        )}
      </div>

      {/* Evaluated Details */}
      {evaluated && (
        <div className="p-4 rounded-2xl bg-slate-900 border border-slate-800 text-xs text-slate-300 space-y-2 animate-fadeIn">
          <span className="font-bold text-white block">Learner Model Mastery Impact:</span>
          <p>{evaluated.explanation}</p>
          <div className="flex items-center gap-2 text-brand-300 font-mono text-[11px] pt-1">
            <span>Concept: {evaluated.concept_id}</span>
            <span>•</span>
            <span>New Mastery: {evaluated.mastery_percentage}% ({evaluated.mastery_delta >= 0 ? '+' : ''}{Math.round(evaluated.mastery_delta * 100)}%)</span>
          </div>
        </div>
      )}
    </div>
  );
}
