import React, { useState } from 'react';
import { LearnerProvider, useLearner } from './context/LearnerContext';
import { VoiceProvider } from './context/VoiceContext';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import WisprFlowModal from './components/WisprFlowModal';

// Pages
import Dashboard from './pages/Dashboard';
import Onboarding from './pages/Onboarding';
import AITutor from './pages/AITutor';
import AdaptiveQuiz from './pages/AdaptiveQuiz';
import MasteryView from './pages/MasteryView';
import MisconceptionAnalysis from './pages/MisconceptionAnalysis';
import PersonalizedPractice from './pages/PersonalizedPractice';
import Analytics from './pages/Analytics';

// Mobile bottom nav icons
import { LayoutDashboard, Bot, BrainCircuit, Network, Dumbbell } from 'lucide-react';

function AppContent() {
  const [currentPage, setCurrentPage] = useState('dashboard');
  const { toast } = useLearner();

  const renderPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard onNavigate={setCurrentPage} />;
      case 'onboarding':
        return <Onboarding onNavigate={setCurrentPage} />;
      case 'tutor':
        return <AITutor onNavigate={setCurrentPage} />;
      case 'quiz':
        return <AdaptiveQuiz onNavigate={setCurrentPage} />;
      case 'mastery':
        return <MasteryView onNavigate={setCurrentPage} />;
      case 'misconceptions':
        return <MisconceptionAnalysis onNavigate={setCurrentPage} />;
      case 'practice':
        return <PersonalizedPractice onNavigate={setCurrentPage} />;
      case 'analytics':
        return <Analytics onNavigate={setCurrentPage} />;
      default:
        return <Dashboard onNavigate={setCurrentPage} />;
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-brand-500 selection:text-white">
      {/* Top Navbar */}
      <Navbar currentPage={currentPage} onNavigate={setCurrentPage} />

      {/* Main Container */}
      <div className="flex-1 flex overflow-hidden">
        {/* Desktop Sidebar */}
        <Sidebar currentPage={currentPage} onNavigate={setCurrentPage} />

        {/* Dynamic Page Content */}
        <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8 pb-20 md:pb-8">
          {renderPage()}
        </main>
      </div>

      {/* Mobile Bottom Navigation Bar */}
      <nav className="md:hidden fixed bottom-0 left-0 right-0 z-40 bg-slate-950/95 border-t border-slate-800 flex items-center justify-around py-2.5 backdrop-blur-lg">
        <button
          onClick={() => setCurrentPage('dashboard')}
          className={`flex flex-col items-center gap-1 text-[10px] font-medium ${
            currentPage === 'dashboard' ? 'text-brand-400 font-bold' : 'text-slate-400'
          }`}
        >
          <LayoutDashboard className="w-4 h-4" />
          <span>Home</span>
        </button>
        <button
          onClick={() => setCurrentPage('tutor')}
          className={`flex flex-col items-center gap-1 text-[10px] font-medium ${
            currentPage === 'tutor' ? 'text-brand-400 font-bold' : 'text-slate-400'
          }`}
        >
          <Bot className="w-4 h-4" />
          <span>Tutor</span>
        </button>
        <button
          onClick={() => setCurrentPage('quiz')}
          className={`flex flex-col items-center gap-1 text-[10px] font-medium ${
            currentPage === 'quiz' ? 'text-brand-400 font-bold' : 'text-slate-400'
          }`}
        >
          <BrainCircuit className="w-4 h-4" />
          <span>Quiz</span>
        </button>
        <button
          onClick={() => setCurrentPage('mastery')}
          className={`flex flex-col items-center gap-1 text-[10px] font-medium ${
            currentPage === 'mastery' ? 'text-brand-400 font-bold' : 'text-slate-400'
          }`}
        >
          <Network className="w-4 h-4" />
          <span>Mastery</span>
        </button>
        <button
          onClick={() => setCurrentPage('practice')}
          className={`flex flex-col items-center gap-1 text-[10px] font-medium ${
            currentPage === 'practice' ? 'text-brand-400 font-bold' : 'text-slate-400'
          }`}
        >
          <Dumbbell className="w-4 h-4" />
          <span>Practice</span>
        </button>
      </nav>

      {/* Global Wispr Flow Integration Modal */}
      <WisprFlowModal />

      {/* Toast Notification */}
      {toast && (
        <div className="fixed bottom-16 md:bottom-6 right-6 z-50 p-4 rounded-2xl bg-brand-600 text-white shadow-2xl animate-bounce text-xs font-semibold flex items-center gap-2">
          <span>{toast.message}</span>
        </div>
      )}
    </div>
  );
}

export default function App() {
  return (
    <LearnerProvider>
      <VoiceProvider>
        <AppContent />
      </VoiceProvider>
    </LearnerProvider>
  );
}
