import React, { useState, useEffect, useRef } from 'react';
import { useLearner } from '../context/LearnerContext';
import { useVoice } from '../context/VoiceContext';
import { api } from '../services/api';
import {
  Send,
  Mic,
  MicOff,
  Volume2,
  VolumeX,
  Zap,
  Sparkles,
  Bot,
  User,
  BookOpen,
  HelpCircle,
  Lightbulb,
} from 'lucide-react';
import AudioVisualizer from '../components/AudioVisualizer';

const QUICK_PROMPTS = [
  "Why is current conserved in a series circuit?",
  "Explain wire stretching resistance: R vs 4R",
  "How does Snell's law work with the marching band analogy?",
  "What is the difference between Fleming's Left and Right Hand rules?",
  "Why is danger signal light always red?"
];

export default function AITutor() {
  const { user, addPoints } = useLearner();
  const {
    isListening,
    transcript,
    setTranscript,
    interimTranscript,
    toggleListening,
    isSpeaking,
    speakText,
    stopSpeaking,
    speechRate,
    setSpeechRate,
    audioLevel,
    setIsWisprModalOpen,
  } = useVoice();

  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'assistant',
      content: "Hello Aarav! I am your VoxLearn AI Physics tutor. We can discuss Electricity, Light, Magnetism, or the Human Eye. You can speak naturally via microphone or Wispr Flow. What concept or problem would you like to explore?",
      topic: 'Physics',
      socratic_stage: 'welcome',
      formulas: [],
      created_at: 'Just now'
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [sending, setSending] = useState(false);
  const [autoSpeak, setAutoSpeak] = useState(true);
  const [activeTopic, setActiveTopic] = useState('Electricity');
  const chatBottomRef = useRef(null);

  // Sync speech transcript into input field
  useEffect(() => {
    if (transcript) {
      setInputText(transcript);
    }
  }, [transcript]);

  useEffect(() => {
    chatBottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, sending]);

  const handleSendMessage = async (textToSend) => {
    const text = (textToSend || inputText).trim();
    if (!text || sending) return;

    const userMsg = {
      id: Date.now(),
      sender: 'user',
      content: text,
      voice_transcribed: isListening,
      created_at: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMsg]);
    setInputText('');
    setTranscript('');
    if (isListening) toggleListening();
    setSending(true);

    try {
      const res = await api.sendTutorMessage({
        user_id: user?.id || 1,
        message: text,
        voice_transcribed: userMsg.voice_transcribed
      });

      const assistantMsg = {
        id: Date.now() + 1,
        sender: 'assistant',
        content: res.content,
        topic: res.topic,
        socratic_stage: res.socratic_stage,
        formulas: res.suggested_formulas || [],
        created_at: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      setMessages(prev => [...prev, assistantMsg]);
      setActiveTopic(res.topic);
      addPoints(15);

      if (autoSpeak) {
        speakText(res.content);
      }
    } catch (err) {
      console.warn('Tutor response fallback:', err);
      const fallbackMsg = {
        id: Date.now() + 1,
        sender: 'assistant',
        content: "That's a thoughtful question! Let's think through the physical principle first: what happens to the charge carrier flow in this scenario? Consider how conservation laws apply here.",
        topic: 'Physics',
        socratic_stage: 'probe',
        formulas: ["V = I * R", "I = Q / t"],
        created_at: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages(prev => [...prev, fallbackMsg]);
      if (autoSpeak) speakText(fallbackMsg.content);
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="h-[calc(100vh-6.5rem)] flex flex-col max-w-5xl mx-auto animate-fadeIn">
      {/* Tutor Header Controls */}
      <div className="p-4 bg-slate-900/80 border border-slate-800 rounded-2xl flex flex-wrap items-center justify-between gap-3 mb-4 shrink-0 shadow-lg">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-gradient-to-br from-brand-500 to-accent-violet rounded-xl text-white shadow-md shadow-brand-500/20">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-sm font-bold text-white flex items-center gap-2">
              Socratic Physics Tutor
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-brand-500/20 text-brand-300 font-mono">
                {activeTopic}
              </span>
            </h1>
            <p className="text-[11px] text-slate-400">Guiding questions • Step-by-step scaffolding</p>
          </div>
        </div>

        {/* Voice Control Buttons */}
        <div className="flex items-center gap-2">
          {/* Wispr Flow Button */}
          <button
            onClick={() => setIsWisprModalOpen(true)}
            className="px-3 py-1.5 rounded-xl bg-slate-950 border border-slate-700 hover:border-brand-500 text-xs text-slate-300 hover:text-white flex items-center gap-1.5 transition-all"
            title="Configure Wispr Flow"
          >
            <Zap className="w-3.5 h-3.5 text-amber-400" />
            <span className="hidden sm:inline font-mono text-[11px]">Wispr Flow</span>
          </button>

          {/* Auto Read-aloud Toggle */}
          <button
            onClick={() => {
              if (isSpeaking) stopSpeaking();
              setAutoSpeak(!autoSpeak);
            }}
            className={`p-2 rounded-xl border text-xs transition-colors flex items-center gap-1.5 ${
              autoSpeak
                ? 'bg-brand-500/20 border-brand-500/40 text-brand-300'
                : 'bg-slate-950 border-slate-800 text-slate-400 hover:text-slate-300'
            }`}
            title={autoSpeak ? 'Auto-Voice Speaking On' : 'Voice Speaking Muted'}
          >
            {autoSpeak ? <Volume2 className="w-4 h-4 text-brand-400" /> : <VolumeX className="w-4 h-4" />}
            <span className="text-[11px] hidden sm:inline">{autoSpeak ? 'TTS On' : 'TTS Muted'}</span>
          </button>

          {/* Audio Visualizer Pill */}
          <AudioVisualizer isActive={isListening} isSpeaking={isSpeaking} level={audioLevel} />
        </div>
      </div>

      {/* Chat Messages Body */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 rounded-2xl bg-slate-950/50 border border-slate-800/80 mb-4">
        {messages.map((m) => {
          const isUser = m.sender === 'user';
          return (
            <div key={m.id} className={`flex gap-3 ${isUser ? 'justify-end' : 'justify-start'}`}>
              {!isUser && (
                <div className="w-8 h-8 rounded-xl bg-gradient-to-br from-brand-500 to-accent-violet flex items-center justify-center text-white shrink-0 shadow-md">
                  <Bot className="w-4 h-4" />
                </div>
              )}

              <div className={`max-w-2xl space-y-2 ${isUser ? 'items-end' : 'items-start'}`}>
                <div
                  className={`p-4 rounded-2xl text-xs sm:text-sm leading-relaxed ${
                    isUser
                      ? 'bg-brand-600 text-white rounded-br-none shadow-md shadow-brand-600/20'
                      : 'bg-slate-900 border border-slate-800 text-slate-200 rounded-bl-none shadow-md'
                  }`}
                >
                  <p className="whitespace-pre-wrap">{m.content}</p>

                  {/* Formulas pill if any */}
                  {m.formulas && m.formulas.length > 0 && (
                    <div className="mt-3 pt-2.5 border-t border-slate-800/80 space-y-1">
                      <span className="text-[10px] font-mono uppercase tracking-wider text-brand-400 font-bold block">
                        Core Physics Formulas:
                      </span>
                      <div className="flex flex-wrap gap-1.5">
                        {m.formulas.map((f, fIdx) => (
                          <span
                            key={fIdx}
                            className="px-2 py-0.5 rounded-md bg-slate-950/80 text-brand-300 font-mono text-[11px] border border-brand-500/20"
                          >
                            {f}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>

                <div className="flex items-center gap-2 px-1 text-[10px] text-slate-400">
                  <span>{m.created_at}</span>
                  {!isUser && (
                    <button
                      onClick={() => speakText(m.content)}
                      className="hover:text-brand-300 flex items-center gap-1 transition-colors"
                      title="Read aloud"
                    >
                      <Volume2 className="w-3 h-3" />
                      <span>Listen</span>
                    </button>
                  )}
                  {m.socratic_stage && (
                    <span className="font-mono text-slate-400 uppercase text-[9px] bg-slate-800 px-1.5 py-0.2 rounded">
                      {m.socratic_stage}
                    </span>
                  )}
                </div>
              </div>

              {isUser && (
                <div className="w-8 h-8 rounded-xl bg-slate-800 border border-slate-700 flex items-center justify-center text-slate-300 shrink-0">
                  <User className="w-4 h-4" />
                </div>
              )}
            </div>
          );
        })}

        {sending && (
          <div className="flex gap-3 items-center text-slate-400 text-xs">
            <div className="w-8 h-8 rounded-xl bg-brand-500/20 text-brand-400 flex items-center justify-center animate-pulse">
              <Bot className="w-4 h-4" />
            </div>
            <div className="flex items-center gap-1.5 px-3 py-2 rounded-xl bg-slate-900 border border-slate-800">
              <span className="w-1.5 h-1.5 bg-brand-400 rounded-full animate-bounce" />
              <span className="w-1.5 h-1.5 bg-brand-400 rounded-full animate-bounce [animation-delay:0.2s]" />
              <span className="w-1.5 h-1.5 bg-brand-400 rounded-full animate-bounce [animation-delay:0.4s]" />
              <span className="ml-1 text-[11px] font-mono">Tutor is reasoning...</span>
            </div>
          </div>
        )}

        <div ref={chatBottomRef} />
      </div>

      {/* Quick Prompts Bar */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2 shrink-0 no-scrollbar">
        <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400 shrink-0 font-mono">
          Explore:
        </span>
        {QUICK_PROMPTS.map((qp, idx) => (
          <button
            key={idx}
            onClick={() => handleSendMessage(qp)}
            className="px-2.5 py-1 rounded-lg bg-slate-900/90 hover:bg-slate-800 border border-slate-800 text-[11px] text-slate-300 hover:text-white whitespace-nowrap transition-colors shrink-0"
          >
            {qp}
          </button>
        ))}
      </div>

      {/* Input Box with Voice & Send Controls */}
      <div className="p-2.5 bg-slate-900/90 border border-slate-800 rounded-2xl shrink-0 shadow-xl">
        {/* Live speech preview if listening */}
        {isListening && interimTranscript && (
          <div className="px-3 py-1.5 mb-2 bg-brand-500/10 border border-brand-500/20 rounded-xl text-xs text-brand-300 font-mono flex items-center gap-2 animate-pulse">
            <Mic className="w-3.5 h-3.5 text-red-400 animate-ping" />
            <span>Hearing: "{interimTranscript}"</span>
          </div>
        )}

        <div className="flex items-center gap-2">
          {/* Main Voice Toggle */}
          <button
            onClick={() => toggleListening()}
            className={`p-3 rounded-xl transition-all shadow-md ${
              isListening
                ? 'bg-red-500 text-white shadow-red-500/30 animate-pulse'
                : 'bg-slate-800 hover:bg-slate-700 text-slate-200 hover:text-white'
            }`}
            title={isListening ? 'Stop listening' : 'Start voice input (or use Wispr Flow)'}
          >
            {isListening ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5 text-brand-400" />}
          </button>

          <input
            type="text"
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
            placeholder={
              isListening
                ? "Listening to speech... Speak freely or dictate via Wispr Flow..."
                : "Ask a physics question, formulate an analogy, or speak with Wispr Flow..."
            }
            className="flex-1 bg-transparent px-3 py-2 text-xs sm:text-sm text-white placeholder-slate-500 focus:outline-none"
          />

          <button
            onClick={() => handleSendMessage()}
            disabled={!inputText.trim() || sending}
            className="p-3 rounded-xl bg-brand-500 hover:bg-brand-600 disabled:opacity-40 disabled:cursor-not-allowed text-white shadow-lg shadow-brand-500/25 transition-all"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
