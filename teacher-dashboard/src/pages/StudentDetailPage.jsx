import React, { useState, useEffect } from 'react';
import DashboardHeader from '../components/DashboardHeader';
import ActivityModal from '../components/ActivityModal';
import { fetchStudentDetail } from '../services/teacherApi';

export default function StudentDetailPage({ studentId, onNavigate }) {
  const [detail, setDetail] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);

  useEffect(() => {
    fetchStudentDetail(studentId || 'student_001').then(setDetail);
  }, [studentId]);

  if (!detail) return <div style={{ padding: '20px' }}>Loading student profile...</div>;

  return (
    <div>
      <div style={{ marginBottom: '16px' }}>
        <button className="btn-secondary" onClick={() => onNavigate('students')}>
          ← Back to Students Roster
        </button>
      </div>

      <DashboardHeader title={`Student Profile: ${detail.name}`} subtitle={detail.course} />

      {/* Header Profile Summary */}
      <div className="card-box">
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px' }}>
          <div>
            <div style={{ fontSize: '13px', color: '#64748B', fontWeight: 600 }}>Overall Mastery</div>
            <div style={{ fontSize: '28px', fontWeight: 800, color: detail.overall_mastery < 60 ? '#DC2626' : '#2563EB' }}>
              {detail.overall_mastery}%
            </div>
          </div>

          <div>
            <div style={{ fontSize: '13px', color: '#64748B', fontWeight: 600 }}>Recent Quiz Score</div>
            <div style={{ fontSize: '28px', fontWeight: 800, color: '#D97706' }}>
              {detail.recent_assessment_score}%
            </div>
          </div>

          <div>
            <div style={{ fontSize: '13px', color: '#64748B', fontWeight: 600 }}>Learning Trend</div>
            <div style={{ fontSize: '20px', fontWeight: 700, color: detail.trend === 'declining' ? '#991B1B' : '#166534' }}>
              {detail.trend === 'declining' ? '↓ Declining' : '↑ Improving'}
            </div>
          </div>

          <div>
            <div style={{ fontSize: '13px', color: '#64748B', fontWeight: 600 }}>Primary Weak Topic</div>
            <div style={{ fontSize: '16px', fontWeight: 700, color: '#DC2626' }}>
              {detail.weak_topics ? detail.weak_topics[0] : 'Process Scheduling'}
            </div>
          </div>
        </div>

        <div style={{ marginTop: '20px', padding: '16px', backgroundColor: '#FEF3C7', borderRadius: '12px', border: '1px solid #FCD34D' }}>
          <strong style={{ color: '#92400E' }}>💡 Recommended Teacher Action:</strong>
          <p style={{ fontSize: '14px', color: '#78350F', marginTop: '4px' }}>{detail.recommended_action}</p>
          <button
            className="btn-primary"
            style={{ marginTop: '12px' }}
            onClick={() => setModalOpen(true)}
          >
            🚀 Create Targeted Revision Activity for {detail.name}
          </button>
        </div>
      </div>

      {/* Subject Performance Breakdown */}
      <div className="grid-2col">
        <div className="card-box">
          <h2 className="section-title">📚 Subject Mastery Breakdown</h2>
          {Object.entries(detail.subject_masteries).map(([subj, score]) => (
            <div key={subj} style={{ marginBottom: '14px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '14px', fontWeight: 600 }}>
                <span>{subj}</span>
                <span>{score}%</span>
              </div>
              <div className="progress-track" style={{ marginTop: '4px' }}>
                <div
                  className={`progress-fill ${score >= 80 ? 'progress-strong' : score >= 60 ? 'progress-moderate' : 'progress-attention'}`}
                  style={{ width: `${score}%` }}
                ></div>
              </div>
            </div>
          ))}
        </div>

        <div className="card-box">
          <h2 className="section-title">🕒 Recent Student Activity Timeline</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {detail.recent_activities.map((act, i) => (
              <div key={i} style={{ padding: '12px', border: '1px solid #E2E8F0', borderRadius: '10px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px', fontWeight: 700, color: '#4F46E5' }}>
                  <span>{act.type.toUpperCase()}</span>
                  <span style={{ color: '#64748B' }}>{act.date}</span>
                </div>
                <div style={{ fontSize: '14px', fontWeight: 600, color: '#0F172A', marginTop: '4px' }}>
                  {act.title}
                </div>
                {act.score && <div style={{ fontSize: '12.5px', color: '#166534', fontWeight: 600 }}>Score: {act.score}</div>}
              </div>
            ))}
          </div>
        </div>
      </div>

      <ActivityModal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        initialData={{ topic: detail.weak_topics ? detail.weak_topics[0] : 'Process Scheduling', subject: 'Operating Systems' }}
      />
    </div>
  );
}
