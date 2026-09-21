import React from 'react';

export default function MisconceptionCard({ item }) {
  return (
    <div
      style={{
        backgroundColor: '#FFFFFF',
        border: '1px solid #E2E8F0',
        borderRadius: '14px',
        padding: '16px',
        marginBottom: '12px'
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
        <span style={{ fontSize: '13px', fontWeight: 700, color: '#4F46E5' }}>
          {item.subject} • {item.topic}
        </span>
        <span style={{ fontSize: '12px', fontWeight: 700, color: '#D97706', backgroundColor: '#FEF3C7', padding: '2px 8px', borderRadius: '4px' }}>
          {item.affected_students_count} Students Affected
        </span>
      </div>

      <div style={{ fontSize: '14.5px', fontWeight: 600, color: '#1E293B', marginBottom: '8px' }}>
        💡 Misconception: "{item.misconception_text}"
      </div>

      <div style={{ fontSize: '13px', color: '#475569' }}>
        <strong>Suggested Resource:</strong> {item.recommended_resource}
      </div>
    </div>
  );
}
