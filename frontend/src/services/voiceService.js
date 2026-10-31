/**
 * Voice Service & Wispr Flow Integration Bridge
 * Supports:
 * - Real-time browser speech recognition (Web Speech API)
 * - Text-to-Speech (TTS) using SpeechSynthesis
 * - Wispr Flow dictation handling & hotkey trigger
 */

class VoiceService {
  constructor() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    this.recognition = SpeechRecognition ? new SpeechRecognition() : null;
    this.isSupported = !!this.recognition;
    this.isListening = false;
    this.onTranscriptCallback = null;
    this.onErrorCallback = null;

    if (this.recognition) {
      this.recognition.continuous = true;
      this.recognition.interimResults = true;
      this.recognition.lang = 'en-US';

      this.recognition.onresult = (event) => {
        let interimTranscript = '';
        let finalTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; ++i) {
          if (event.results[i].isFinal) {
            finalTranscript += event.results[i][0].transcript;
          } else {
            interimTranscript += event.results[i][0].transcript;
          }
        }

        if (this.onTranscriptCallback) {
          this.onTranscriptCallback({
            final: finalTranscript.trim(),
            interim: interimTranscript.trim(),
            fullText: (finalTranscript + ' ' + interimTranscript).trim(),
          });
        }
      };

      this.recognition.onerror = (err) => {
        console.warn('Speech recognition event:', err.error);
        if (this.onErrorCallback) this.onErrorCallback(err);
      };

      this.recognition.onend = () => {
        this.isListening = false;
      };
    }
  }

  startListening(onTranscript, onError) {
    if (!this.isSupported) {
      if (onError) onError(new Error('Speech recognition not supported in this browser. You can type or use Wispr Flow.'));
      return false;
    }

    this.onTranscriptCallback = onTranscript;
    this.onErrorCallback = onError;

    try {
      this.recognition.start();
      this.isListening = true;
      return true;
    } catch (e) {
      console.warn('Speech recognition already started or error:', e);
      return false;
    }
  }

  stopListening() {
    if (this.recognition && this.isListening) {
      try {
        this.recognition.stop();
      } catch (e) {}
      this.isListening = false;
    }
  }

  speak(text, { onEnd, rate = 1.0, pitch = 1.0 } = {}) {
    if (!window.speechSynthesis) return;

    // Cancel any ongoing speech
    window.speechSynthesis.cancel();

    // Clean markdown symbols for cleaner pronunciation
    const cleanText = text
      .replace(/[*#_`>~]/g, '')
      .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1')
      .replace(/\n+/g, ' ');

    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.rate = rate;
    utterance.pitch = pitch;

    // Pick best English voice if available
    const voices = window.speechSynthesis.getVoices();
    const naturalVoice = voices.find(v => v.lang.startsWith('en') && (v.name.includes('Natural') || v.name.includes('Google') || v.name.includes('Samantha')));
    if (naturalVoice) {
      utterance.voice = naturalVoice;
    }

    if (onEnd) utterance.onend = onEnd;
    window.speechSynthesis.speak(utterance);
  }

  stopSpeaking() {
    if (window.speechSynthesis) {
      window.speechSynthesis.cancel();
    }
  }
}

export const voiceService = new VoiceService();
