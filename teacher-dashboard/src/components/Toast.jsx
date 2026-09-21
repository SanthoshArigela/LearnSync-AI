import React, { createContext, useContext, useState, useCallback } from 'react';
import { XIcon, CheckCircleIcon, AlertCircleIcon, InfoIcon } from './Icons';

const ToastContext = createContext(null);

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);

  const addToast = useCallback((message, type = 'info', duration = 4000) => {
    const id = Date.now() + Math.random().toString(36).substring(2, 9);
    setToasts((prev) => [...prev, { id, message, type }]);

    if (duration > 0) {
      setTimeout(() => {
        removeToast(id);
      }, duration);
    }
    return id;
  }, []);

  const removeToast = useCallback((id) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  const toast = {
    success: (msg, dur) => addToast(msg, 'success', dur),
    info: (msg, dur) => addToast(msg, 'info', dur),
    warning: (msg, dur) => addToast(msg, 'warning', dur),
    error: (msg, dur) => addToast(msg, 'error', dur),
    remove: removeToast
  };

  return (
    <ToastContext.Provider value={toast}>
      {children}
      <div className="toast-container" aria-live="polite" role="region" aria-label="Notifications">
        {toasts.map((t) => (
          <div key={t.id} className={`toast-item toast-${t.type}`} role="status">
            <span className="toast-icon">
              {t.type === 'success' && <CheckCircleIcon size={18} />}
              {t.type === 'error' && <AlertCircleIcon size={18} />}
              {t.type === 'warning' && <AlertCircleIcon size={18} />}
              {t.type === 'info' && <InfoIcon size={18} />}
            </span>
            <span className="toast-message">{t.message}</span>
            <button
              className="toast-close-btn"
              onClick={() => removeToast(t.id)}
              aria-label="Close notification"
            >
              <XIcon size={14} />
            </button>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}

export function useToast() {
  const context = useContext(ToastContext);
  if (!context) {
    // Fallback if rendered outside provider
    return {
      success: (msg) => console.log('[Toast Success]:', msg),
      info: (msg) => console.log('[Toast Info]:', msg),
      warning: (msg) => console.log('[Toast Warning]:', msg),
      error: (msg) => console.log('[Toast Error]:', msg),
      remove: () => {}
    };
  }
  return context;
}
