// Centralized frontend configuration
// Allows overriding backend URL via Vite env variable VITE_BACKEND_URL

export const API_BASE: string = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000';

export const HEALTH_ENDPOINT = `${API_BASE}/health`;
export const GENERATE_ENDPOINT = `${API_BASE}/llm/generate`;

export const GENERATION_TIMEOUT = 30000; // 30s timeout
export const RETRY_COUNT = 3;
