import React from 'react';
import DashboardHeader from '../components/DashboardHeader';
import Button from '../components/Button';
import { LogoutIcon } from '../components/Icons';

export default function ProfilePage({ onLogout }) {
  return (
    <div>
      <DashboardHeader title="Teacher Profile & Settings" subtitle="Classroom Configuration & System Parameters" />

      <div className="grid-2col">
        {/* Faculty Information Card */}
        <div className="card-box" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
          <div>
            <h2 className="section-title">👤 Faculty Information</h2>
            <div style={{ display: 'flex', gap: '18px', alignItems: 'center', marginBottom: '20px' }}>
              <div style={{
                width: '60px',
                height: '60px',
                borderRadius: '16px',
                backgroundColor: '#4F46E5',
                color: 'white',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '22px',
                fontWeight: 800,
                boxShadow: '0 4px 12px rgba(79, 70, 229, 0.25)'
              }}>
                DR
              </div>
              <div>
                <div style={{ fontSize: '19px', fontWeight: 800, color: '#0F172A' }}>Dr. R. Sharma</div>
                <div style={{ fontSize: '13.5px', color: '#64748B', fontWeight: 500 }}>Associate Professor, Department of CSE</div>
                <div style={{ fontSize: '12.5px', color: '#4F46E5', fontWeight: 700, marginTop: '2px' }}>LearnSync AI Licensed Instructor</div>
              </div>
            </div>

            <div style={{ borderTop: '1px solid #E2E8F0', paddingTop: '16px', display: 'flex', flexDirection: 'column', gap: '10px', fontSize: '13.5px', color: '#334155', marginBottom: '24px' }}>
              <div><strong>Assigned Course:</strong> B.Tech Computer Science & Engineering</div>
              <div><strong>Specialization:</strong> AI & Machine Learning</div>
              <div><strong>Active Section:</strong> Section A (Semester 5)</div>
              <div><strong>Enrolled Class Strength:</strong> 42 Students</div>
            </div>
          </div>

          {/* Account Actions Section */}
          {onLogout && (
            <div style={{ borderTop: '1px solid #E2E8F0', paddingTop: '18px', marginTop: 'auto' }}>
              <div style={{ fontSize: '12px', fontWeight: 700, color: '#64748B', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '10px' }}>
                Account Actions
              </div>
              <Button
                variant="danger"
                size="md"
                icon={<LogoutIcon size={16} />}
                onClick={onLogout}
              >
                Sign Out
              </Button>
            </div>
          )}
        </div>

        {/* System Status & Product Identity Card */}
        <div className="card-box" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
          <div>
            <h2 className="section-title">⚡ LearnSync AI Engine Status</h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: '24px' }}>
              <div style={{ padding: '12px 16px', backgroundColor: '#F0FDF4', border: '1px solid #86EFAC', borderRadius: '10px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontSize: '13.5px', fontWeight: 600, color: '#166534' }}>FastAPI Backend Endpoint</span>
                <span style={{ fontSize: '12px', fontWeight: 700, color: '#15803D' }}>● Connected (127.0.0.1:8000)</span>
              </div>

              <div style={{ padding: '12px 16px', backgroundColor: '#F0FDF4', border: '1px solid #86EFAC', borderRadius: '10px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontSize: '13.5px', fontWeight: 600, color: '#166534' }}>AI Provider Abstraction</span>
                <span style={{ fontSize: '12px', fontWeight: 700, color: '#15803D' }}>Gemini + Local AI Ready</span>
              </div>

              <div style={{ padding: '12px 16px', backgroundColor: '#EFF6FF', border: '1px solid #BFDBFE', borderRadius: '10px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontSize: '13.5px', fontWeight: 600, color: '#1E40AF' }}>Student Sync Channel</span>
                <span style={{ fontSize: '12px', fontWeight: 700, color: '#1D4ED8' }}>Real-Time Sync Operational</span>
              </div>
            </div>
          </div>

          {/* About LearnSync AI Product Card */}
          <div style={{
            borderTop: '1px solid #E2E8F0',
            paddingTop: '18px',
            marginTop: 'auto'
          }}>
            <div style={{ fontSize: '12px', fontWeight: 700, color: '#64748B', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '12px' }}>
              About LearnSync AI
            </div>
            <div style={{ display: 'flex', gap: '14px', alignItems: 'flex-start' }}>
              <img
                src="/assets/learnsync-ai-logo.png"
                alt="LearnSync AI"
                style={{ width: '48px', height: '48px', borderRadius: '12px', objectFit: 'contain', flexShrink: 0 }}
              />
              <div style={{ flex: 1 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2px' }}>
                  <span style={{ fontSize: '17px', fontWeight: 800, color: '#0F172A' }}>LearnSync AI</span>
                  <span style={{
                    fontSize: '11px',
                    fontWeight: 700,
                    padding: '3px 8px',
                    borderRadius: '12px',
                    backgroundColor: '#EEF2FF',
                    color: '#3730A3',
                    border: '1px solid #C7D2FE'
                  }}>
                    v1.0 • Operational
                  </span>
                </div>
                <div style={{ fontSize: '13px', fontWeight: 600, color: '#4F46E5', marginBottom: '4px' }}>
                  Connecting Every Learner to Smarter Learning
                </div>
                <div style={{ fontSize: '12.5px', color: '#64748B', lineHeight: 1.4 }}>
                  AI-powered personalized learning platform for students and educators.
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
