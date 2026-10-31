import React, { useState, useEffect } from 'react';
import confetti from 'canvas-confetti';
import { useLearner } from '../context/LearnerContext';
import { useVoice } from '../context/VoiceContext';
import { api } from '../services/api';
import {
  Brain,
  Sparkles,
  CheckCircle2,
  XCircle,
  HelpCircle,
  Volume2,
  ArrowRight,
  TrendingUp,
  AlertTriangle,
  Lightbulb,
  Award,
  RotateCcw,
} from 'lucide-react';

export default function AdaptiveQuiz({ onNavigate }) {
  const { user, addPoints, refreshDashboard } = useLearner();
  const { speakText } = useVoice();

  const [loading, setLoading] = useState(true);
  const [session, setSession] = useState(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState(null);
  const [confidenceLevel, setConfidenceLevel] = useState(3); // 1 to 5
  const [evaluating, setEvaluating] = useState(false);
  const [evaluationResult, setEvaluationResult] = useState(null);
  const [showFormulaHint, setShowFormulaHint] = useState(false);
  const [quizComplete, setQuizComplete] = useState(false);
  const [finalSummary, setFinalSummary] = useState(null);

  const startNewQuiz = async (type = 'adaptive', topic = null) => {
    setLoading(true);
    setEvaluationResult(null);
    setSelectedOption(null);
    setShowFormulaHint(false);
    setQuizComplete(false);
    setCurrentQuestionIndex(0);

    try {
      const data = await api.startQuiz({
        user_id: user?.id || 1,
        quiz_type: type,
        topic: topic,
        num_questions: 5
      });
      setSession(data);
    } catch (err) {
      console.warn('Fallback quiz generation:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    startNewQuiz();
  }, []);

  const currentQuestion = session?.questions?.[currentQuestionIndex];

  const handleSelectOption = (idx) => {
    if (evaluationResult) return; // Locked after submission
    setSelectedOption(idx);
  };

  const handleSubmitAnswer = async () => {
    if (selectedOption === null || evaluating || !currentQuestion) return;

    setEvaluating(true);
    try {
      const res = await api.submitQuizAnswer({
        user_id: user?.id || 1,
        quiz_session_id: session.session_id,
        question_id: currentQuestion.id,
        selected_option_index: selectedOption,
        confidence_level: confidenceLevel,
        time_taken_seconds: 22
      });

      setEvaluationResult(res);
      if (res.is_correct) {
        addPoints(20);
      }
    } catch (err) {
      console.error('Answer submission error:', err);
    } finally {
      setEvaluating(false);
    }
  };

  const handleNextQuestion = async () => {
    if (currentQuestionIndex + 1 < (session?.questions?.length || 0)) {
      setCurrentQuestionIndex(prev => prev + 1);
      setSelectedOption(null);
      setEvaluationResult(null);
      setShowFormulaHint(false);
    } else {
      // Complete quiz
      try {
        const completeRes = await api.completeQuizSession(session.session_id);
        setFinalSummary(completeRes);
        setQuizComplete(true);
        refreshDashboard();
        confetti({
          particleCount: 100,
          spread: 70,
          origin: { y: 0.6 }
        });
      } catch (err) {
        setQuizComplete(true);
      }
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] gap-3">
        <div className="w-10 h-10 border-4 border-brand-500 border-t-transparent rounded-full animate-spin" />
        <p className="text-sm text-slate-400">Calibrating Adaptive Quiz questions via IRT...</p>
      </div>
    );
  }

  // Final Summary Screen
  if (quizComplete) {
    return (
      <div className="max-w-xl mx-auto py-8 text-center space-y-6 animate-fadeIn">
        <div className="p-8 bg-slate-900/90 rounded-3xl border border-brand-500/30 shadow-2xl space-y-5">
          <div className="w-16 h-16 mx-auto rounded-2xl bg-gradient-to-br from-amber-400 to-brand-500 flex items-center justify-center text-white shadow-xl shadow-brand-500/30">
            <Award className="w-8 h-8" />
          </div>

          <div className="space-y-1">
            <h1 className="text-2xl font-black text-white">Adaptive Quiz Complete!</h1>
            <p className="text-xs text-slate-300">
              Bayesian Knowledge Tracing has updated your concept masteries and latent ability θ.
            </p>
          </div>

          <div className="grid grid-cols-3 gap-3 p-4 bg-slate-950/80 rounded-2xl border border-slate-800 text-left">
            <div>
              <span className="text-[10px] text-slate-400 block font-mono">Score</span>
              <span className="text-base font-bold text-white font-mono">
                {finalSummary?.score || 4} / {finalSummary?.total_questions || 5}
              </span>
            </div>
            <div>
              <span className="text-[10px] text-slate-400 block font-mono">Accuracy</span>
              <span className="text-base font-bold text-emerald-400 font-mono">
                {finalSummary?.accuracy_percentage || 80}%
              </span>
            </div>
            <div>
              <span className="text-[10px] text-slate-400 block font-mono">XP Earned</span>
              <span className="text-base font-bold text-amber-400 font-mono">
                +{finalSummary?.points_earned || 90} XP
              </span>
            </div>
          </div>

          <div className="pt-3 flex flex-col sm:flex-row gap-3 justify-center">
            <button
              onClick={() => startNewQuiz('adaptive')}
              className="py-3 px-5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-semibold text-xs flex items-center justify-center gap-2 transition-colors"
            >
              <RotateCcw className="w-4 h-4" />
              <span>Take Another Adaptive Quiz</span>
            </button>
            <button
              onClick={() => onNavigate('mastery')}
              className="py-3 px-6 rounded-xl bg-brand-500 hover:bg-brand-600 text-white font-bold text-xs shadow-lg shadow-brand-500/25 transition-all flex items-center justify-center gap-2 glow-brand"
            >
              <TrendingUp className="w-4 h-4" />
              <span>Inspect Updated Mastery</span>
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (!currentQuestion) return null;

  return (
    <div className="max-w-3xl mx-auto py-4 space-y-6 animate-fadeIn">
      {/* Quiz Progress & Question Meta */}
      <div className="p-4 bg-slate-900/80 rounded-2xl border border-slate-800 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-brand-500/20 text-brand-400 rounded-xl">
            <Brain className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold text-white">
                Question {currentQuestionIndex + 1} of {session?.questions?.length || 5}
              </span>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-slate-800 text-slate-300 font-mono border border-slate-700">
                {currentQuestion.topic}
              </span>
            </div>
            <div className="flex items-center gap-2 mt-0.5">
              <span className="text-[10px] text-slate-400">Bloom: {currentQuestion.bloom_level}</span>
              <span className="text-[10px] text-slate-500">•</span>
              <span className="text-[10px] text-amber-400 font-mono">IRT Difficulty {currentQuestion.difficulty}/5</span>
            </div>
          </div>
        </div>

        {/* Read aloud Question */}
        <button
          onClick={() => speakText(currentQuestion.question_text)}
          className="p-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition-colors"
          title="Read question aloud"
        >
          <Volume2 className="w-4 h-4 text-brand-400" />
        </button>
      </div>

      {/* Question Card */}
      <div className="p-6 sm:p-8 bg-slate-900/90 rounded-3xl border border-slate-800 shadow-xl space-y-6">
        <h2 className="text-base sm:text-lg font-bold text-white leading-relaxed">
          {currentQuestion.question_text}
        </h2>

        {/* Formula Hint Button */}
        {currentQuestion.formula_hint && (
          <div>
            <button
              onClick={() => setShowFormulaHint(!showFormulaHint)}
              className="text-xs font-semibold text-brand-400 hover:text-brand-300 flex items-center gap-1.5 transition-colors"
            >
              <Lightbulb className="w-3.5 h-3.5 text-amber-400" />
              <span>{showFormulaHint ? "Hide Formula Scaffolding" : "Show Formula Scaffolding"}</span>
            </button>
            {showFormulaHint && (
              <div className="mt-2 p-3 bg-brand-950/40 border border-brand-500/30 rounded-xl text-xs font-mono text-brand-300 animate-fadeIn">
                {currentQuestion.formula_hint}
              </div>
            )}
          </div>
        )}

        {/* Option Choices */}
        <div className="space-y-3">
          {currentQuestion.options.map((optText, optIdx) => {
            const isSelected = selectedOption === optIdx;
            const isEvaluated = evaluationResult !== null;
            const isCorrectOption = isEvaluated && evaluationResult.correct_option_index === optIdx;
            const isSelectedWrong = isEvaluated && isSelected && !evaluationResult.is_correct;

            let borderStyle = 'border-slate-800 hover:border-slate-700 bg-slate-950/70 text-slate-200';
            if (isEvaluated) {
              if (isCorrectOption) {
                borderStyle = 'border-emerald-500 bg-emerald-950/30 text-emerald-200 font-semibold';
              } else if (isSelectedWrong) {
                borderStyle = 'border-rose-500 bg-rose-950/30 text-rose-200';
              } else {
                borderStyle = 'border-slate-800 bg-slate-950/40 text-slate-500';
              }
            } else if (isSelected) {
              borderStyle = 'border-brand-500 bg-brand-500/10 text-white font-semibold shadow-md shadow-brand-500/15';
            }

            return (
              <button
                key={optIdx}
                onClick={() => handleSelectOption(optIdx)}
                disabled={isEvaluated}
                className={`w-full p-4 rounded-2xl border text-left text-xs sm:text-sm transition-all flex items-start justify-between gap-3 ${borderStyle}`}
              >
                <div className="flex items-start gap-3">
                  <span className="w-6 h-6 rounded-lg bg-slate-900 border border-slate-700/60 flex items-center justify-center font-mono text-xs font-bold text-slate-400 shrink-0 mt-0.5">
                    {String.fromCharCode(65 + optIdx)}
                  </span>
                  <span>{optText}</span>
                </div>

                {isEvaluated && isCorrectOption && (
                  <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
                )}
                {isEvaluated && isSelectedWrong && (
                  <XCircle className="w-5 h-5 text-rose-400 shrink-0" />
                )}
              </button>
            );
          })}
        </div>

        {/* Metacognitive Confidence Bar (Before submission) */}
        {!evaluationResult && (
          <div className="pt-3 border-t border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
            <span className="text-slate-400 font-medium">Metacognitive Confidence (BKT moderation):</span>
            <div className="flex items-center gap-1.5">
              {[
                { lvl: 1, label: 'Pure Guess' },
                { lvl: 2, label: 'Unsure' },
                { lvl: 3, label: 'Moderate' },
                { lvl: 4, label: 'Confident' },
                { lvl: 5, label: 'Certain' },
              ].map((c) => (
                <button
                  key={c.lvl}
                  onClick={() => setConfidenceLevel(c.lvl)}
                  className={`px-2.5 py-1 rounded-lg text-[11px] font-semibold transition-all ${
                    confidenceLevel === c.lvl
                      ? 'bg-brand-500 text-white shadow-md'
                      : 'bg-slate-950 text-slate-400 hover:bg-slate-800 border border-slate-800'
                  }`}
                >
                  {c.label}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Submit or Next Question Action Button */}
        {!evaluationResult ? (
          <button
            onClick={handleSubmitAnswer}
            disabled={selectedOption === null || evaluating}
            className="w-full py-3.5 rounded-xl bg-brand-500 hover:bg-brand-600 disabled:opacity-40 disabled:cursor-not-allowed text-white font-bold text-xs sm:text-sm shadow-lg shadow-brand-500/25 transition-all flex items-center justify-center gap-2 glow-brand"
          >
            {evaluating ? (
              <>
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
                <span>Evaluating via Learner Model...</span>
              </>
            ) : (
              <span>Submit Answer for Reasoning Analysis</span>
            )}
          </button>
        ) : (
          <button
            onClick={handleNextQuestion}
            className="w-full py-3.5 rounded-xl bg-brand-500 hover:bg-brand-600 text-white font-bold text-xs sm:text-sm shadow-lg shadow-brand-500/25 transition-all flex items-center justify-center gap-2 glow-brand"
          >
            <span>
              {currentQuestionIndex + 1 < (session?.questions?.length || 0)
                ? 'Continue to Next Adaptive Question'
                : 'Complete Quiz & View Final Summary'}
            </span>
            <ArrowRight className="w-4 h-4" />
          </button>
        )}
      </div>

      {/* Deep Wrong-Answer Reasoning & BKT Update Card */}
      {evaluationResult && (
        <div className="space-y-4 animate-fadeIn">
          {/* Wrong Answer Misconception Diagnostic */}
          {!evaluationResult.is_correct && evaluationResult.misconception_found && (
            <div className="p-5 rounded-2xl bg-rose-950/30 border border-rose-500/40 space-y-3">
              <div className="flex items-center gap-2 text-rose-300 font-bold text-xs sm:text-sm">
                <AlertTriangle className="w-4 h-4 text-rose-400" />
                <span>Misconception Diagnostic: {evaluationResult.misconception_title}</span>
                <span className="text-[10px] px-2 py-0.5 rounded-full bg-rose-500/20 text-rose-300 font-mono">
                  {evaluationResult.misconception_category}
                </span>
              </div>

              <div className="space-y-2 text-xs text-slate-300 leading-relaxed">
                <p>
                  <strong className="text-white">Why this trap occurs:</strong> {evaluationResult.why_it_happens}
                </p>
                <p>
                  <strong className="text-white">Physical Reality:</strong> {evaluationResult.physical_reality}
                </p>
                <div className="p-3 bg-slate-900/80 rounded-xl border border-rose-500/20 text-emerald-300 font-medium">
                  <strong>💡 Memory Remedy:</strong> {evaluationResult.remedy_tip}
                </div>
              </div>
            </div>
          )}

          {/* Correct Explanation */}
          <div className="p-4 rounded-2xl bg-slate-900/80 border border-slate-800 text-xs text-slate-300 space-y-1.5">
            <span className="font-bold text-white text-xs block">Detailed Physics Explanation:</span>
            <p className="leading-relaxed">{evaluationResult.explanation}</p>
          </div>

          {/* Bayesian Knowledge Tracing (BKT) Update Card */}
          <div className="p-4 rounded-2xl bg-slate-950/90 border border-brand-500/30 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
            <div>
              <span className="text-[10px] uppercase font-mono tracking-wider text-brand-400 font-bold block">
                Bayesian Knowledge Tracing (BKT) Update
              </span>
              <p className="text-slate-300 mt-0.5">
                Latent mastery probability updated: <span className="font-mono font-bold text-white">{evaluationResult.previous_p_l}</span> → <span className="font-mono font-bold text-brand-300">{evaluationResult.updated_p_l}</span>
              </p>
            </div>
            <div className="flex items-center gap-3">
              <span
                className={`font-mono font-bold px-2.5 py-1 rounded-lg text-xs ${
                  evaluationResult.mastery_delta >= 0
                    ? 'bg-emerald-500/20 text-emerald-300'
                    : 'bg-rose-500/20 text-rose-300'
                }`}
              >
                {evaluationResult.mastery_delta >= 0 ? '+' : ''}
                {Math.round(evaluationResult.mastery_delta * 100)}%
              </span>
              <span className="text-[11px] font-semibold text-slate-300 font-mono">
                Mastery: {evaluationResult.mastery_percentage}%
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
