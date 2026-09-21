// Frontend authentication service for LearnSync AI Web Platform

const SESSION_KEY = 'learnsync_session';
const API_URL = 'http://localhost:8000/api/auth/login';

export const authService = {
  async login(email, password, role) {
    const cleanEmail = (email || '').trim().toLowerCase();
    const cleanPassword = (password || '').trim();
    const cleanRole = (role || 'student').trim().toLowerCase();

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email: cleanEmail,
          password: cleanPassword,
          role: cleanRole,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        if (data.authenticated && data.user) {
          const session = {
            authenticated: true,
            user: data.user,
            loginTime: new Date().toISOString(),
          };
          localStorage.setItem(SESSION_KEY, JSON.stringify(session));
          return { success: true, user: data.user };
        }
      } else {
        const errorData = await response.json().catch(() => ({}));
        return {
          success: false,
          message: errorData.detail || 'Invalid email or password',
        };
      }
    } catch (err) {
      console.warn('Backend API unreachable, using controlled demo validation:', err);
    }

    // Controlled client-side fallback for hackathon demo resilience
    if (cleanEmail === 'student@learnsync.ai' && cleanPassword === 'student123' && cleanRole === 'student') {
      const user = { id: 'std_001', name: 'Santhosh', email: cleanEmail, role: 'student' };
      const session = { authenticated: true, user, loginTime: new Date().toISOString() };
      localStorage.setItem(SESSION_KEY, JSON.stringify(session));
      return { success: true, user };
    }

    if (cleanEmail === 'faculty@learnsync.ai' && cleanPassword === 'faculty123' && cleanRole === 'faculty') {
      const user = { id: 'fac_001', name: 'Prof. R. Sharma', email: cleanEmail, role: 'faculty' };
      const session = { authenticated: true, user, loginTime: new Date().toISOString() };
      localStorage.setItem(SESSION_KEY, JSON.stringify(session));
      return { success: true, user };
    }

    return {
      success: false,
      message: 'Invalid email or password for the selected role',
    };
  },

  logout() {
    localStorage.removeItem(SESSION_KEY);
  },

  getSession() {
    try {
      const raw = localStorage.getItem(SESSION_KEY);
      if (!raw) return null;
      const parsed = JSON.parse(raw);
      if (parsed && parsed.authenticated && parsed.user) {
        return parsed;
      }
    } catch (e) {
      localStorage.removeItem(SESSION_KEY);
    }
    return null;
  },

  isAuthenticated() {
    return !!this.getSession();
  },

  getRole() {
    const session = this.getSession();
    return session ? session.user.role : null;
  },

  getUser() {
    const session = this.getSession();
    return session ? session.user : null;
  },
};
