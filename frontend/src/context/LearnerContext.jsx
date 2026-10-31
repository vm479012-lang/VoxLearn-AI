import React, { createContext, useContext, useState, useEffect } from 'react';
import { api } from '../services/api';

const LearnerContext = createContext();

export function LearnerProvider({ children }) {
  const [user, setUser] = useState(null);
  const [dashboard, setDashboard] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [toast, setToast] = useState(null);

  const showToast = (message, type = 'info') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 4000);
  };

  const refreshDashboard = async () => {
    try {
      setLoading(true);
      const data = await api.getDashboardSummary(1);
      setDashboard(data);
      setUser(data.user);
      setError(null);
    } catch (err) {
      console.warn('Could not load dashboard data from backend:', err);
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    refreshDashboard();
  }, []);

  const addPoints = (pts) => {
    if (user) {
      setUser(prev => ({ ...prev, points: prev.points + pts }));
    }
  };

  return (
    <LearnerContext.Provider
      value={{
        user,
        setUser,
        dashboard,
        loading,
        error,
        refreshDashboard,
        addPoints,
        toast,
        showToast,
      }}
    >
      {children}
    </LearnerContext.Provider>
  );
}

export function useLearner() {
  return useContext(LearnerContext);
}
