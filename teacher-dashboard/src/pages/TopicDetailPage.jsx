import React, { useState, useEffect } from 'react';
import DashboardHeader from '../components/DashboardHeader';
import ActivityModal from '../components/ActivityModal';
import { fetchTopicDetail } from '../services/teacherApi';

export default function TopicDetailPage({ topicId, onNavigate }) {
  const [detail, setDetail] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);

  useEffect(() => {
    fetchTopicDetail(topicId || 'topic_os_sched').then(setDetail);
  }, [topicId]);

  if (!detail) return <div style={{ padding: '20px' }}>Loading topic intelligence...</div>;

  return (
    <div>
      <div style={{ marginBottom: '16px' }}>
        <button className="btn-secondary" onClick={() => onNavigate('topics')}>
          ← Back to Topics List
        </button>
      </div>

      <DashboardHeader title={`Topic Deep Dive: ${detail.topic}`} subtitle={`Subject: ${detail.subject}`} />

      {/* Overview Stat Cards */}
      <div className="card-box">
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px' }}>
          <div>
            <div style={{ fontSize: '13px', color: '#64748B', fontWeight: 600 }}>Class Mastery</div>
            <div style={{ fontSize: '28px', fontWeight: 800, color: detail.class_mastery < 60 ? '#DC2626' : '#2563EB' }}>
              {detail.class_mastery}%
            </div>
          </div>

          <div>
            <div style={{ fontSize: '13px', color: '#64748B', fontWeight: 600 }}>Affected Students</div>
            <div style={{ fontSize: '28px', fontWeight: 800, color: '#D97706' }}>
              {detail.affected_students_count}
            </div>
          </div>

          <div>
            <div style={{ fontSize: '13px', color: '#64748B', fontWeight: 600 }}>Severity Priority</div>
            <div style={{ marginTop: '6px' }}>
              <span className={`severity-tag ${detail.severity}`} style={{ fontSize: '14px', padding: '4px 12px' }}>
                {detail.severity} Priority
              </span>
            </div>
          </div>

          <div>
            <div style={{ fontSize: '13px', color: '#64748B', fontWeight: 600 }}>Performance Trend</div>
            <div style={{ fontSize: '20px', fontWeight: 700, color: detail.trend === 'declining' ? '#991B1B' : '#166534', marginTop: '4px' }}>
              {detail.trend === 'declining' ? '↓ Declining' : '↑ Improving'}
            </div>
          </div>
        </div>

        <div style={{ marginTop: '20px', padding: '16px', backgroundColor: '#EFF6FF', borderRadius: '12px', border: '1px solid #BFDBFE' }}>
          <strong style={{ color: '#1E40AF' }}>💡 Recommended Teacher Action:</strong>
          <p style={{ fontSize: '14px', color: '#1E3A8A', marginTop: '4px' }}>"{detail.recommended_teaching_action}"</p>
          <button
            className="btn-primary"
            style={{ marginTop: '12px' }}
            onClick={() => setModalOpen(true)}
          >
            🚀 Create 5-Question Revision Activity for {detail.topic}
          </button>
        </div>
      </div>

      <div className="grid-2col">
        {/* Mastery Distribution */}
        <div className="card-box">
          <h2 className="section-title">📊 Class Mastery Distribution</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13.5px', fontWeight: 600 }}>
                <span style={{ color: '#166534' }}>Strong (≥ 80%)</span>
                <span>{detail.mastery_distribution?.strong || 12} Students</span>
              </div>
              <div className="progress-track" style={{ marginTop: '4px' }}>
                <div className="progress-fill progress-strong" style={{ width: `${((detail.mastery_distribution?.strong || 12) / 42) * 100}%` }}></div>
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13.5px', fontWeight: 600 }}>
                <span style={{ color: '#1D4ED8' }}>Moderate (60% - 79%)</span>
                <span>{detail.mastery_distribution?.moderate || 13} Students</span>
              </div>
              <div className="progress-track" style={{ marginTop: '4px' }}>
                <div className="progress-fill progress-moderate" style={{ width: `${((detail.mastery_distribution?.moderate || 13) / 42) * 100}%` }}></div>
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13.5px', fontWeight: 600 }}>
                <span style={{ color: '#991B1B' }}>Needs Practice (&lt; 60%)</span>
                <span>{detail.affected_students_count} Students</span>
              </div>
              <div className="progress-track" style={{ marginTop: '4px' }}>
                <div className="progress-fill progress-attention" style={{ width: `${(detail.affected_students_count / 42) * 100}%` }}></div>
              </div>
            </div>
          </div>
        </div>

        {/* Common Misconceptions */}
        <div className="card-box">
          <h2 className="section-title">💡 Common Misconceptions & Mistakes</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {detail.common_mistakes && detail.common_mistakes.map((m, i) => (
              <div key={i} style={{ padding: '12px', backgroundColor: '#FFFBEB', borderRadius: '10px', border: '1px solid #FDE68A' }}>
                <div style={{ fontSize: '13.5px', fontWeight: 700, color: '#92400E' }}>
                  Misconception #{i + 1}
                </div>
                <div style={{ fontSize: '14px', color: '#78350F', marginTop: '4px' }}>
                  "{m}"
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Struggling Students Roster */}
      <div className="card-box">
        <h2 className="section-title">👥 Struggling Students on {detail.topic}</h2>
        <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
          {detail.struggling_students && detail.struggling_students.map((name, i) => (
            <div
              key={i}
              style={{
                padding: '8px 14px',
                backgroundColor: '#FEF2F2',
                border: '1px solid #FCA5A5',
                borderRadius: '8px',
                fontSize: '13.5px',
                fontWeight: 600,
                color: '#991B1B',
                cursor: 'pointer'
              }}
              onClick={() => onNavigate('students')}
            >
              👤 {name}
            </div>
          ))}
        </div>
      </div>

      <ActivityModal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        initialData={{ topic: detail.topic, subject: detail.subject }}
      />
    </div>
  );
}
