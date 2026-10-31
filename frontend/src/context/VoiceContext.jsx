import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { voiceService } from '../services/voiceService';

const VoiceContext = createContext();

export function VoiceProvider({ children }) {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [interimTranscript, setInterimTranscript] = useState('');
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [speechRate, setSpeechRate] = useState(1.0);
  const [wisprFlowActive, setWisprFlowActive] = useState(true);
  const [isWisprModalOpen, setIsWisprModalOpen] = useState(false);
  const [audioLevel, setAudioLevel] = useState(0);

  // Simulated audio meter pulse when listening or speaking
  useEffect(() => {
    let interval = null;
    if (isListening || isSpeaking) {
      interval = setInterval(() => {
        setAudioLevel(Math.floor(Math.random() * 80) + 20);
      }, 100);
    } else {
      setAudioLevel(0);
    }
    return () => clearInterval(interval);
  }, [isListening, isSpeaking]);

  const toggleListening = useCallback((onResultText) => {
    if (isListening) {
      voiceService.stopListening();
      setIsListening(false);
      setInterimTranscript('');
    } else {
      setTranscript('');
      setInterimTranscript('');
      const started = voiceService.startListening(
        (res) => {
          setInterimTranscript(res.interim);
          if (res.final) {
            setTranscript((prev) => (prev ? prev + ' ' + res.final : res.final));
            if (onResultText) onResultText(res.final);
          }
        },
        (err) => {
          console.warn('Voice error:', err);
          setIsListening(false);
        }
      );
      if (started) setIsListening(true);
    }
  }, [isListening]);

  const speakText = useCallback((text) => {
    if (!text) return;
    setIsSpeaking(true);
    voiceService.speak(text, {
      rate: speechRate,
      onEnd: () => setIsSpeaking(false),
    });
  }, [speechRate]);

  const stopSpeaking = useCallback(() => {
    voiceService.stopSpeaking();
    setIsSpeaking(false);
  }, []);

  const injectWisprDictation = useCallback((dictatedText) => {
    setTranscript((prev) => (prev ? prev + ' ' + dictatedText : dictatedText));
  }, []);

  return (
    <VoiceContext.Provider
      value={{
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
        wisprFlowActive,
        setWisprFlowActive,
        isWisprModalOpen,
        setIsWisprModalOpen,
        audioLevel,
        injectWisprDictation,
      }}
    >
      {children}
    </VoiceContext.Provider>
  );
}

export function useVoice() {
  return useContext(VoiceContext);
}
