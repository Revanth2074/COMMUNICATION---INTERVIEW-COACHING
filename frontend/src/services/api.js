import axios from 'axios';
import toast from 'react-hot-toast';

// API service for Interview Coach
const API = {
  // Base URL (set in App.js via axios.defaults.baseURL)
  
  // Authentication
  register: async (userData) => {
    try {
      const response = await axios.post('/auth/register', userData);
      return response.data;
    } catch (error) {
      const message = error.response?.data?.detail || 
                     error.response?.data?.message ||
                     'Registration failed';
      toast.error(message);
      throw error;
    }
  },

  login: async (username, password) => {
    try {
      const response = await axios.post('/auth/token', {
        username,
        password
      }, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      });
      return response.data;
    } catch (error) {
      const message = error.response?.data?.detail || 
                     error.response?.data?.message ||
                     'Login failed';
      toast.error(message);
      throw error;
    }
  },

  getCurrentUser: async () => {
    try {
      const response = await axios.get('/auth/me');
      return response.data.data;
    } catch (error) {
      throw error;
    }
  },

  // Candidates
  createCandidate: async (candidateData) => {
    try {
      const response = await axios.post('/candidates/', candidateData);
      return response.data;
    } catch (error) {
      const message = error.response?.data?.detail || 
                     error.response?.data?.message ||
                     'Failed to create candidate';
      toast.error(message);
      throw error;
    }
  },

  getCandidate: async (candidateId) => {
    try {
      const response = await axios.get(`/candidates/${candidateId}`);
      return response.data.data;
    } catch (error) {
      throw error;
    }
  },

  getCurrentCandidate: async () => {
    try {
      const response = await axios.get('/candidates/me');
      return response.data.data;
    } catch (error) {
      throw error;
    }
  },

  updateCandidate: async (candidateId, candidateData) => {
    try {
      const response = await axios.put(`/candidates/${candidateId}`, candidateData);
      return response.data;
    } catch (error) {
      const message = error.response?.data?.detail || 
                     error.response?.data?.message ||
                     'Failed to update candidate';
      toast.error(message);
      throw error;
    }
  },

  // Questions
  getQuestions: async (params = {}) => {
    try {
      const response = await axios.get('/questions/', { params });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getQuestion: async (questionId) => {
    try {
      const response = await axios.get(`/questions/${questionId}`);
      return response.data.data;
    } catch (error) {
      throw error;
    }
  },

  getRandomQuestion: async (params = {}) => {
    try {
      const response = await axios.get('/questions/random', { params });
      return response.data.data;
    } catch (error) {
      throw error;
    }
  },

  getQuestionsByRole: async (role) => {
    try {
      const response = await axios.get(`/questions/roles?role=${role}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getQuestionStats: async () => {
    try {
      const response = await axios.get('/questions/stats');
      return response.data.data;
    } catch (error) {
      throw error;
    }
  },

  // Sessions
  createSession: async (sessionData) => {
    try {
      const response = await axios.post('/sessions/', sessionData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getSession: async (sessionId) => {
    try {
      const response = await axios.get(`/sessions/${sessionId}`);
      return response.data.data;
    } catch (error) {
      throw error;
    }
  },

  getSessionsByCandidate: async (candidateId, params = {}) => {
    try {
      const response = await axios.get(`/sessions/candidate/${candidateId}`, { params });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getActiveSession: async (candidateId) => {
    try {
      const response = await axios.get(`/sessions/active/${candidateId}`);
      return response.data.data;
    } catch (error) {
      throw error;
    }
  },

  completeSession: async (sessionId) => {
    try {
      const response = await axios.post(`/sessions/${sessionId}/complete`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Responses
  createResponse: async (responseData) => {
    try {
      const response = await axios.post('/responses/', responseData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getResponsesBySession: async (sessionId) => {
    try {
      const response = await axios.get(`/responses/session/${sessionId}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getResponsesByCandidate: async (candidateId, params = {}) => {
    try {
      const response = await axios.get(`/responses/candidate/${candidateId}`, { params });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getLatestResponse: async (candidateId) => {
    try {
      const response = await axios.get(`/responses/candidate/${candidateId}/latest`);
      return response.data.data;
    } catch (error) {
      throw error;
    }
  },

  // Feedback
  createFeedback: async (feedbackData) => {
    try {
      const response = await axios.post('/feedback/', feedbackData);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getFeedback: async (feedbackId) => {
    try {
      const response = await axios.get(`/feedback/${feedbackId}`);
      return response.data.data;
    } catch (error) {
      throw error;
    }
  },

  getFeedbackByResponse: async (responseId) => {
    try {
      const response = await axios.get(`/feedback/response/${responseId}`);
      return response.data.data;
    } catch (error) {
      throw error;
    }
  },

  getFeedbackBySession: async (sessionId) => {
    try {
      const response = await axios.get(`/feedback/session/${sessionId}`);
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getFeedbackByCandidate: async (candidateId, params = {}) => {
    try {
      const response = await axios.get(`/feedback/candidate/${candidateId}`, { params });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getAverageScores: async (candidateId) => {
    try {
      const response = await axios.get(`/feedback/candidate/${candidateId}/average-scores`);
      return response.data.data;
    } catch (error) {
      throw error;
    }
  },

  // Multi-agent analysis
  analyzeResponse: async (params) => {
    try {
      const response = await axios.post('/feedback/analyze', null, { params });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  quickAnalyzeResponse: async (responseText, question) => {
    try {
      const response = await axios.post('/feedback/quick-analyze', null, {
        params: { response_text: responseText, question }
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Agents
  getAgentStatus: async () => {
    try {
      const response = await axios.get('/agents/status');
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  startPracticeSession: async (params) => {
    try {
      const response = await axios.post('/agents/practice/start', null, { params });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  analyzePracticeResponse: async (params) => {
    try {
      const response = await axios.post('/agents/practice/analyze', null, { params });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getFollowUpQuestion: async (params) => {
    try {
      const response = await axios.post('/agents/follow-up', null, { params });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  generateImprovementPlan: async (params) => {
    try {
      const response = await axios.post('/agents/improvement-plan', null, { params });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Individual agent analysis
  analyzeCommunication: async (responseText, question) => {
    try {
      const response = await axios.get('/agents/communication/analyze', {
        params: { response_text: responseText, question }
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  analyzeContent: async (responseText, question) => {
    try {
      const response = await axios.get('/agents/content/analyze', {
        params: { response_text: responseText, question }
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  analyzeSTAR: async (responseText, question) => {
    try {
      const response = await axios.get('/agents/star/analyze', {
        params: { response_text: responseText, question }
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  generateSTARExample: async (question) => {
    try {
      const response = await axios.get('/agents/star/example', {
        params: { question }
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  // Progress
  getProgressSummary: async (candidateId) => {
    try {
      const response = await axios.get(`/progress/candidate/${candidateId}/summary`);
      return response.data.data;
    } catch (error) {
      throw error;
    }
  },

  getProgressByCandidate: async (candidateId, params = {}) => {
    try {
      const response = await axios.get(`/progress/candidate/${candidateId}`, { params });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  getImprovementAreas: async (candidateId, threshold = 70) => {
    try {
      const response = await axios.get(`/progress/candidate/${candidateId}/improvement-areas`, {
        params: { threshold }
      });
      return response.data.data;
    } catch (error) {
      throw error;
    }
  },

  // Voice
  transcribeAudio: async (audioFile) => {
    try {
      const formData = new FormData();
      formData.append('audio_file', audioFile);
      
      const response = await axios.post('/voice/transcribe', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      return response.data;
    } catch (error) {
      throw error;
    }
  },

  uploadVoiceResponse: async (audioFile, sessionId, candidateId, questionId) => {
    try {
      const formData = new FormData();
      formData.append('audio_file', audioFile);
      
      const response = await axios.post(
        `/voice/upload?session_id=${sessionId}&candidate_id=${candidateId}&question_id=${questionId}`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      );
      return response.data;
    } catch (error) {
      throw error;
    }
  }
};

export default API;
