import React from 'react';
import Button from './Button';
import { LogoutIcon } from './Icons';

export default function SidebarNav({ activeTab, setActiveTab, onLogout }) {
  const items = [
    { id: 'dashboard', label: 'Dashboard', icon: '📊' },
    { id: 'students', label: 'Students', icon: '👨‍🎓' },
    { id: 'topics', label: 'Topics', icon: '📚' },
    { id: 'assessments', label: 'Assessments', icon: '📝' },
    { id: 'recommendations', label: 'Recommendations', icon: '💡' },
    { id: 'profile', label: 'Profile', icon: '⚙️' },
  ];

  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-icon">
          <img src="/assets/learnsync-ai-logo.png" alt="LearnSync AI" style={{ width: '100%', height: '100%', borderRadius: '10px', objectFit: 'contain' }} />
        </div>
        <div>
          <div className="brand-title">LearnSync AI</div>
          <div className="brand-subtitle">Teacher Intelligence</div>
        </div>
      </div>
      <ul className="nav-menu">
        {items.map((item) => (
          <li key={item.id}>
            <a
              href={`#/faculty/${item.id}`}
              className={`nav-item ${activeTab === item.id ? 'active' : ''}`}
              onClick={(e) => {
                e.preventDefault();
                setActiveTab(item.id);
                window.location.hash = `/faculty/${item.id}`;
              }}
            >
              <span className="nav-icon">{item.icon}</span>
              <span>{item.label}</span>
            </a>
          </li>
        ))}
      </ul>

      <div style={{ marginTop: 'auto', paddingTop: '16px', borderTop: '1px solid #E2E8F0' }}>
        <Button
          variant="danger"
          size="sm"
          fullWidth
          icon={<LogoutIcon size={15} />}
          onClick={onLogout}
          style={{ marginBottom: '12px' }}
        >
          Sign Out
        </Button>
        <div style={{ fontSize: '11px', fontWeight: 700, color: '#4F46E5', marginBottom: '2px' }}>
          LearnSync AI Web Platform
        </div>
        <div style={{ fontSize: '10.5px', color: '#64748B', lineHeight: 1.3 }}>
          Connecting Every Learner to Smarter Learning
        </div>
      </div>
    </aside>
  );
}
