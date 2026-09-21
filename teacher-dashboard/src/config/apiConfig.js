// Centralized Production-Ready API & WebSocket Configuration for LearnSync AI

const getEnvVar = (key, fallback) => {
  if (typeof import.meta !== 'undefined' && import.meta.env && import.meta.env[key]) {
    return import.meta.env[key];
  }
  return fallback;
};

// In development with Vite proxy, API_BASE_URL defaults to empty string '' for relative '/api' calls.
// In production, VITE_API_BASE_URL can be provided via environment variables (e.g. 'https://api.learnsync.ai').
export const API_BASE_URL = getEnvVar('VITE_API_BASE_URL', '');

export const getApiUrl = (path) => {
  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  return `${API_BASE_URL}${cleanPath}`;
};

export const getWsUrl = (path) => {
  const customWsHost = getEnvVar('VITE_WS_BASE_URL', '');
  if (customWsHost) {
    const cleanPath = path.startsWith('/') ? path : `/${path}`;
    return `${customWsHost}${cleanPath}`;
  }

  // Map WebSocket protocol dynamically to match current origin (ws:// or wss://)
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  // Use current window host or fallback to location hostname + 8000 port
  const host = window.location.host.includes('5173')
    ? window.location.hostname + ':8000'
    : window.location.host || 'localhost:8000';

  const cleanPath = path.startsWith('/') ? path : `/${path}`;
  return `${protocol}//${host}${cleanPath}`;
};
