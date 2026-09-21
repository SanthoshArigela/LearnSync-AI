import React, { useState, useEffect } from 'react';
import DashboardHeader from '../components/DashboardHeader';
import ActivityModal from '../components/ActivityModal';
import { fetchAssessments } from '../services/teacherApi';

export default function AssessmentsPage({ onNavigate }) {
  const [assessments, setAssessments] = useState([]);
  const [selectedAssessment, setSelectedAssessment] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);

  useEffect(() => {
    fetchAssessments().then((data) => {
      setAssessments(data);
      if (data && data.length > 0) setSelectedAssessment(data[0]);
    });
  }, []);

  return (
    <div>
      <DashboardHeader title="Assessment Analytics" subtitle="Classroom Quiz & Test Performance Diagnostics" />

      <div className="grid-2col">
        {/* Assessment List */}
        <div className="card-box">
          <h2 className="section-title">📝 Recent Assessments</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {assessments.map((a) => (
              <div
                key={a.id}
                onClick={() => setSelectedAssessment(a)}
                style={{
                  padding: '16px',
                  borderRadius: '12px',
                  border: `2px solid ${selectedAssessment?.id === a.id ? '#4F46E5' : '#E2E8F0'}`,
                  backgroundColor: selectedAssessment?.id === a.id ? '#EEF2FF' : '#FFFFFF',
                  cursor: 'pointer',
                  transition: 'all 0.15s ease'
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontSize: '15px', fontWeight: 700, color: '#0F172A' }}>{a.title}</span>
                  <span style={{ fontSize: '12.5px', fontWeight: 600, color: '#64748B' }}>{a.subject}</span>
                </div>
                <div style={{ display: 'flex', gap: '16px', marginTop: '10px', fontSize: '13px', color: '#475569' }}>
                  <span><strong>Average Score:</strong> <span style={{ color: a.average_score < 60 ? '#DC2626' : '#166534', fontWeight: 800 }}>{a.average_score}%</span></span>
                  <span><strong>Completion Rate:</strong> {a.completion_rate}%</span>
                  <span><strong>Students:</strong> {a.total_students}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Selected Assessment Diagnostics */}
        {selectedAssessment ? (
          <div className="card-box">
            <h2 className="section-title">🔍 Diagnostic Breakdown</h2>
            <div style={{ marginBottom: '16px' }}>
              <div style={{ fontSize: '18px', fontWeight: 700, color: '#0F172A' }}>{selectedAssessment.title}</div>
              <div style={{ fontSize: '13.5px', color: '#64748B' }}>Topic: {selectedAssessment.topic}</div>
            </div>

            <div style={{ padding: '16px', backgroundColor: '#FEF2F2', borderRadius: '12px', border: '1px solid #FCA5A5', marginBottom: '16px' }}>
              <div style={{ fontSize: '13px', fontWeight: 700, color: '#991B1B' }}>⚠️ Most Difficult Question</div>
              <div style={{ fontSize: '14px', color: '#7F1D1D', marginTop: '4px', fontWeight: 500 }}>
                "{selectedAssessment.most_difficult_question}"
              </div>
            </div>

            <div style={{ padding: '16px', backgroundColor: '#FFFBEB', borderRadius: '12px', border: '1px solid #FCD34D', marginBottom: '20px' }}>
              <div style={{ fontSize: '13px', fontWeight: 700, color: '#92400E' }}>💡 Primary Weak Concept</div>
              <div style={{ fontSize: '14px', color: '#78350F', marginTop: '4px', fontWeight: 600 }}>
                {selectedAssessment.most_difficult_concept}
              </div>
            </div>

            <button
              className="btn-primary"
              style={{ width: '100%', justifyContent: 'center' }}
              onClick={() => setModalOpen(true)}
            >
              🚀 Create Follow-up Quiz for {selectedAssessment.topic}
            </button>
          </div>
        ) : (
          <div className="card-box">Select an assessment to view diagnostics</div>
        )}
      </div>

      <ActivityModal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        initialData={selectedAssessment ? { topic: selectedAssessment.topic, subject: selectedAssessment.subject } : null}
      />
    </div>
  );
}
