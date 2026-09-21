import React, { useState, useEffect } from 'react';
import DashboardHeader from '../components/DashboardHeader';
import ActivityModal from '../components/ActivityModal';
import { fetchTopics } from '../services/teacherApi';

export default function TopicsPage({ onNavigate }) {
  const [topics, setTopics] = useState([]);
  const [search, setSearch] = useState('');
  const [modalOpen, setModalOpen] = useState(false);
  const [modalData, setModalData] = useState(null);

  useEffect(() => {
    fetchTopics().then(setTopics);
  }, []);

  const filtered = topics.filter(t =>
    t.topic.toLowerCase().includes(search.toLowerCase()) ||
    t.subject.toLowerCase().includes(search.toLowerCase())
  );

  const handleCreateActivity = (t) => {
    setModalData(t);
    setModalOpen(true);
  };

  return (
    <div>
      <DashboardHeader title="Topic Intelligence" subtitle="Classroom Topic Mastery & Weakness Analysis" />

      <div className="card-box" style={{ marginBottom: '20px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <input
            type="text"
            className="form-control"
            style={{ width: '320px' }}
            placeholder="Search topics or subjects..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <span style={{ fontSize: '13px', fontWeight: 600, color: '#64748B' }}>
            {filtered.length} Active Classroom Topics
          </span>
        </div>
      </div>

      <div className="card-box" style={{ padding: 0, overflow: 'hidden' }}>
        <table className="data-table">
          <thead>
            <tr>
              <th>Topic</th>
              <th>Subject</th>
              <th>Class Mastery</th>
              <th>Struggling Students</th>
              <th>Trend</th>
              <th>Priority</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((t) => (
              <tr key={t.id}>
                <td>
                  <a
                    href={`#topic-${t.id}`}
                    onClick={(e) => {
                      e.preventDefault();
                      onNavigate('topic-detail', t.id);
                    }}
                    style={{ color: '#4F46E5', fontWeight: 700, textDecoration: 'none' }}
                  >
                    {t.topic}
                  </a>
                </td>
                <td>{t.subject}</td>
                <td>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span style={{ fontWeight: 700, width: '36px' }}>{t.class_mastery}%</span>
                    <div className="progress-track" style={{ width: '100px' }}>
                      <div
                        className={`progress-fill ${t.class_mastery >= 80 ? 'progress-strong' : t.class_mastery >= 60 ? 'progress-moderate' : 'progress-attention'}`}
                        style={{ width: `${t.class_mastery}%` }}
                      ></div>
                    </div>
                  </div>
                </td>
                <td>
                  <span style={{ color: t.affected_students_count > 10 ? '#DC2626' : '#475569', fontWeight: 700 }}>
                    👥 {t.affected_students_count} students
                  </span>
                </td>
                <td>
                  <span style={{ color: t.trend === 'declining' ? '#DC2626' : t.trend === 'improving' ? '#166534' : '#64748B', fontWeight: 700 }}>
                    {t.trend === 'declining' ? '↓ Declining' : t.trend === 'improving' ? '↑ Improving' : '→ Stable'}
                  </span>
                </td>
                <td>
                  <span className={`severity-tag ${t.severity}`}>{t.severity}</span>
                </td>
                <td>
                  <div style={{ display: 'flex', gap: '8px' }}>
                    <button
                      className="btn-secondary"
                      style={{ fontSize: '12px', padding: '6px 10px' }}
                      onClick={() => onNavigate('topic-detail', t.id)}
                    >
                      🔍 Inspect
                    </button>
                    <button
                      className="btn-primary"
                      style={{ fontSize: '12px', padding: '6px 10px' }}
                      onClick={() => handleCreateActivity(t)}
                    >
                      🚀 Revise
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <ActivityModal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        initialData={modalData}
      />
    </div>
  );
}
