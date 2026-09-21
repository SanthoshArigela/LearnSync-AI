import React from 'react';

export default function StudentAttentionTable({ students, onSelectStudent, onCreateActivity }) {
  if (!students || students.length === 0) return null;

  return (
    <div className="card-box" style={{ overflowX: 'auto' }}>
      <h2 className="section-title">🚨 Students Needing Attention</h2>
      <table className="data-table">
        <thead>
          <tr>
            <th>Student Name</th>
            <th>Overall Mastery</th>
            <th>Weak Topic</th>
            <th>Trend</th>
            <th>Recommended Action</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {students.map((student) => (
            <tr key={student.student_id}>
              <td style={{ fontWeight: 600 }}>{student.name}</td>
              <td style={{ fontWeight: 700, color: student.overall_mastery < 60 ? '#DC2626' : '#D97706' }}>
                {student.overall_mastery}%
              </td>
              <td>{student.weak_topic}</td>
              <td>
                <span
                  style={{
                    fontWeight: 700,
                    color: student.trend === 'improving' ? '#166534' : student.trend === 'declining' ? '#991B1B' : '#475569'
                  }}
                >
                  {student.trend === 'improving' ? '↑ Improving' : student.trend === 'declining' ? '↓ Declining' : '→ Stable'}
                </span>
              </td>
              <td style={{ fontSize: '13px', color: '#475569' }}>{student.recommended_action}</td>
              <td>
                <div style={{ display: 'flex', gap: '8px' }}>
                  <button
                    className="btn-secondary"
                    style={{ fontSize: '12px', padding: '4px 10px' }}
                    onClick={() => onSelectStudent && onSelectStudent(student.student_id)}
                  >
                    View
                  </button>
                  {onCreateActivity && (
                    <button
                      className="btn-secondary"
                      style={{ fontSize: '12px', padding: '4px 10px', backgroundColor: '#EEF2FF', color: '#4F46E5', borderColor: '#C7D2FE' }}
                      onClick={() => onCreateActivity({ topic: student.weak_topic, subject: 'Computer Science' })}
                    >
                      Assign
                    </button>
                  )}
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
