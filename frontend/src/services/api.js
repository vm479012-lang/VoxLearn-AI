/**
 * API Service for VoxLearn AI
 * Communicates with FastAPI backend with seamless error handling.
 */

const API_BASE_URL = '/api';

async function request(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  try {
    const res = await fetch(url, config);
    if (!res.ok) {
      const errorData = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(errorData.detail || `Request failed with status ${res.status}`);
    }
    return await res.json();
  } catch (err) {
    console.error(`API Error on [${options.method || 'GET'} ${url}]:`, err);
    throw err;
  }
}

export const api = {
  // User & Onboarding
  getUserProfile: (userId = 1) => request(`/user/profile?user_id=${userId}`),
  completeOnboarding: (data) => request('/user/onboarding', {
    method: 'POST',
    body: JSON.stringify(data),
  }),

  // Dashboard
  getDashboardSummary: (userId = 1) => request(`/dashboard/summary?user_id=${userId}`),

  // AI Tutor
  sendTutorMessage: (data) => request('/tutor/message', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  listConversations: (userId = 1) => request(`/tutor/conversations?user_id=${userId}`),
  getConversationHistory: (convId) => request(`/tutor/conversation/${convId}`),

  // Adaptive Quiz
  startQuiz: (data) => request('/quiz/start', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  submitQuizAnswer: (data) => request('/quiz/submit_answer', {
    method: 'POST',
    body: JSON.stringify(data),
  }),
  completeQuizSession: (sessionId) => request(`/quiz/complete/${sessionId}`, {
    method: 'POST',
  }),

  // Concept Mastery & Knowledge Graph
  getMasteryOverview: (userId = 1) => request(`/mastery/overview?user_id=${userId}`),
  getKnowledgeGraph: (userId = 1) => request(`/mastery/graph?user_id=${userId}`),
  getConceptDetail: (conceptId, userId = 1) => request(`/mastery/concept/${conceptId}?user_id=${userId}`),

  // Personalized Practice & Misconceptions
  getMisconceptions: (userId = 1) => request(`/practice/misconceptions?user_id=${userId}`),
  getWeakWorkout: (userId = 1) => request(`/practice/weak_workout?user_id=${userId}`),
  getAnalytics: (userId = 1) => request(`/practice/analytics?user_id=${userId}`),
};
