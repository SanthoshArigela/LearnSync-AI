import React, { useState } from 'react';
import { authService } from '../services/authService';
import Button from '../components/Button';
import { useToast } from '../components/Toast';

export default function LoginPage({ onLoginSuccess }) {
  const toast = useToast();
  const [role, setRole] = useState('student');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [rememberMe, setRememberMe] = useState(true);
  const [errorMessage, setErrorMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage('');

    if (!email.trim() || !password.trim()) {
      setErrorMessage('Please enter both Email and Password.');
      return;
    }

    setLoading(true);
    const result = await authService.login(email, password, role);
    setLoading(false);

    if (result.success) {
      onLoginSuccess(result.user);
    } else {
      setErrorMessage(result.message || 'Authentication failed. Please check credentials.');
    }
  };

  const fillDemo = (demoRole) => {
    setErrorMessage('');
    if (demoRole === 'student') {
      setRole('student');
      setEmail('student@learnsync.ai');
      setPassword('student123');
    } else {
      setRole('faculty');
      setEmail('faculty@learnsync.ai');
      setPassword('faculty123');
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: '#0F172A',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '24px 16px',
      fontFamily: "'Plus Jakarta Sans', sans-serif"
    }}>
      <div style={{
        width: '100%',
        maxWidth: '440px',
        backgroundColor: '#FFFFFF',
        borderRadius: '24px',
        boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.4)',
        padding: '36px 32px',
        border: '1px solid #E2E8F0'
      }}>
        {/* Brand Header */}
        <div style={{ textAlign: 'center', marginBottom: '28px' }}>
          <img
            src="/assets/learnsync-ai-logo.png"
            alt="LearnSync AI"
            className="login-logo"
            style={{
              maxWidth: '72px',
              maxHeight: '72px',
              width: '100%',
              height: 'auto',
              borderRadius: '16px',
              objectFit: 'contain',
              marginBottom: '12px',
              boxShadow: '0 8px 20px rgba(79, 70, 229, 0.15)'
            }}
          />
          <h1 style={{ fontSize: '24px', fontWeight: 800, color: '#0F172A', margin: 0 }}>
            LearnSync AI
          </h1>
          <p style={{ fontSize: '13.5px', color: '#64748B', marginTop: '6px', fontWeight: 500 }}>
            Connecting Every Learner to Smarter Learning
          </p>
        </div>

        {/* Role Selector Tabs */}
        <div style={{
          display: 'flex',
          backgroundColor: '#F1F5F9',
          padding: '4px',
          borderRadius: '14px',
          marginBottom: '24px'
        }}>
          <button
            type="button"
            onClick={() => { setRole('student'); setErrorMessage(''); }}
            style={{
              flex: 1,
              padding: '10px 16px',
              borderRadius: '10px',
              border: 'none',
              fontSize: '14px',
              fontWeight: 700,
              cursor: 'pointer',
              transition: 'all 0.2s ease',
              backgroundColor: role === 'student' ? '#FFFFFF' : 'transparent',
              color: role === 'student' ? '#4F46E5' : '#64748B',
              boxShadow: role === 'student' ? '0 2px 8px rgba(0,0,0,0.08)' : 'none'
            }}
          >
            👨‍🎓 Student
          </button>
          <button
            type="button"
            onClick={() => { setRole('faculty'); setErrorMessage(''); }}
            style={{
              flex: 1,
              padding: '10px 16px',
              borderRadius: '10px',
              border: 'none',
              fontSize: '14px',
              fontWeight: 700,
              cursor: 'pointer',
              transition: 'all 0.2s ease',
              backgroundColor: role === 'faculty' ? '#FFFFFF' : 'transparent',
              color: role === 'faculty' ? '#4F46E5' : '#64748B',
              boxShadow: role === 'faculty' ? '0 2px 8px rgba(0,0,0,0.08)' : 'none'
            }}
          >
            👨‍🏫 Faculty
          </button>
        </div>

        {/* Error Alert */}
        {errorMessage && (
          <div style={{
            padding: '12px 16px',
            backgroundColor: '#FEF2F2',
            border: '1px solid #FCA5A5',
            borderRadius: '12px',
            color: '#B91C1C',
            fontSize: '13px',
            fontWeight: 600,
            marginBottom: '20px',
            display: 'flex',
            alignItems: 'center',
            gap: '8px'
          }}>
            <span>⚠️</span>
            <span>{errorMessage}</span>
          </div>
        )}

        {/* Login Form */}
        <form onSubmit={handleSubmit}>
          {/* Email / User ID */}
          <div style={{ marginBottom: '18px' }}>
            <label style={{
              display: 'block',
              fontSize: '13px',
              fontWeight: 700,
              color: '#334155',
              marginBottom: '6px'
            }}>
              Email Address / User ID
            </label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder={role === 'student' ? 'student@learnsync.ai' : 'faculty@learnsync.ai'}
              required
              style={{
                width: '100%',
                padding: '12px 16px',
                borderRadius: '12px',
                border: '1px solid #CBD5E1',
                fontSize: '14px',
                color: '#0F172A',
                outline: 'none',
                boxSizing: 'border-box',
                transition: 'border 0.2s'
              }}
            />
          </div>

          {/* Password */}
          <div style={{ marginBottom: '18px' }}>
            <label style={{
              display: 'block',
              fontSize: '13px',
              fontWeight: 700,
              color: '#334155',
              marginBottom: '6px'
            }}>
              Password
            </label>
            <div style={{ position: 'relative' }}>
              <input
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
                style={{
                  width: '100%',
                  padding: '12px 42px 12px 16px',
                  borderRadius: '12px',
                  border: '1px solid #CBD5E1',
                  fontSize: '14px',
                  color: '#0F172A',
                  outline: 'none',
                  boxSizing: 'border-box'
                }}
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                style={{
                  position: 'absolute',
                  right: '12px',
                  top: '50%',
                  transform: 'translateY(-50%)',
                  background: 'none',
                  border: 'none',
                  cursor: 'pointer',
                  fontSize: '16px',
                  color: '#64748B'
                }}
                title={showPassword ? 'Hide password' : 'Show password'}
              >
                {showPassword ? '👁️' : '🔒'}
              </button>
            </div>
          </div>

          {/* Options Row */}
          <div style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginBottom: '24px',
            fontSize: '13px'
          }}>
            <label style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#475569', cursor: 'pointer' }}>
              <input
                type="checkbox"
                checked={rememberMe}
                onChange={(e) => setRememberMe(e.target.checked)}
                style={{ accentColor: '#4F46E5' }}
              />
              Remember me
            </label>
            <a
              href="#forgot-password"
              onClick={(e) => { e.preventDefault(); toast.info('For hackathon demonstration, please use the provided demo credentials.'); }}
              style={{ color: '#4F46E5', textDecoration: 'none', fontWeight: 600 }}
            >
              Forgot password?
            </a>
          </div>

          {/* Submit Button */}
          <Button
            type="submit"
            disabled={loading}
            variant="primary"
            size="lg"
            fullWidth
          >
            {loading ? 'Authenticating...' : `Sign In as ${role === 'student' ? 'Student' : 'Faculty'}`}
          </Button>
        </form>

        {/* Quick Demo Credentials Section */}
        <div style={{
          marginTop: '28px',
          paddingTop: '20px',
          borderTop: '1px solid #E2E8F0',
          textAlign: 'center'
        }}>
          <div style={{ fontSize: '11.5px', fontWeight: 700, color: '#64748B', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '12px' }}>
            ⚡ Instant Demo Credentials
          </div>
          <div style={{ display: 'flex', gap: '10px', justifyContent: 'center' }}>
            <Button
              type="button"
              variant="secondary"
              size="sm"
              onClick={() => fillDemo('student')}
            >
              🎓 Student Demo
            </Button>
            <Button
              type="button"
              variant="secondary"
              size="sm"
              onClick={() => fillDemo('faculty')}
            >
              🏫 Faculty Demo
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
