import React from 'react';

export default function LiveClassroomFeed({ events, onSelectStudent, onViewTopic }) {
  const getEventBadge = (type) => {
    switch (type) {
      case 'ASSESSMENT_COMPLETED':
        return { bg: '#D1FAE5', text: '#065F46', icon: '🟢', label: 'Assessment Completed' };
      case 'WEAK_TOPIC_DETECTED':
        return { bg: '#FEF3C7', text: '#92400E', icon: '🟠', label: 'Weak Topic Alert' };
      case 'REPEATED_MISTAKE':
        return { bg: '#FEE2E2', text: '#991B1B', icon: '🔴', label: 'Repeated Misconception' };
      case 'START_REVISION':
        return { bg: '#EEF2FF', text: '#3730A3', icon: '🚀', label: 'Teacher Action Sent' };
      default:
        return { bg: '#E0F2FE', text: '#0369A1', icon: '🔵', label: type.replace('_', ' ') };
    }
  };

  return (
    <div className="card-box">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
        <h2 className="section-title" style={{ margin: 0 }}>
          ⚡ Live Classroom Feed
        </h2>
        <span style={{ fontSize: '12px', color: '#64748B', fontWeight: 600 }}>
          {events.length} Real-Time Stream Events
        </span>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', maxHeight: '420px', overflowY: 'auto', paddingRight: '4px' }}>
        {events.length === 0 ? (
          <div style={{ padding: '20px', textAlign: 'center', color: '#94A3B8', fontSize: '13.5px' }}>
            Listening for student classroom activity...
          </div>
        ) : (
          events.map((evt) => {
            const badge = getEventBadge(evt.event_type);
            return (
              <div
                key={evt.event_id}
                style={{
                  padding: '12px 16px',
                  borderRadius: '12px',
                  border: '1px solid #E2E8F0',
                  backgroundColor: '#FFFFFF',
                  display: 'flex',
                  justify: 'space-between',
                  alignItems: 'center'
                }}
              >
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span
                      style={{
                        padding: '2px 8px',
                        borderRadius: '6px',
                        fontSize: '11px',
                        fontWeight: 700,
                        backgroundColor: badge.bg,
                        color: badge.text,
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '4px'
                      }}
                    >
                      {badge.icon} {badge.label}
                    </span>

                    <span
                      style={{ fontSize: '13.5px', fontWeight: 700, color: '#0F172A', cursor: 'pointer' }}
                      onClick={() => onSelectStudent && onSelectStudent(evt.student_id)}
                    >
                      👤 {evt.student_name}
                    </span>
                  </div>

                  <div style={{ fontSize: '13.5px', color: '#334155', marginTop: '4px', fontWeight: 600 }}>
                    {evt.subject} — <span style={{ color: '#4F46E5' }}>{evt.topic}</span>
                    {evt.subtopic && <span style={{ color: '#64748B', fontWeight: 500 }}> ({evt.subtopic})</span>}
                  </div>

                  {evt.payload && evt.payload.message && (
                    <div style={{ fontSize: '12.5px', color: '#475569', marginTop: '2px' }}>
                      {evt.payload.message}
                    </div>
                  )}
                </div>

                <div style={{ textAlign: 'right' }}>
                  {evt.score !== null && evt.score !== undefined && (
                    <div
                      style={{
                        fontSize: '16px',
                        fontWeight: 800,
                        color: evt.score >= 80 ? '#166534' : evt.score >= 60 ? '#2563EB' : '#DC2626'
                      }}
                    >
                      {evt.score}%
                    </div>
                  )}
                  <div style={{ fontSize: '11px', color: '#94A3B8', marginTop: '2px' }}>
                    {evt.timestamp}
                  </div>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}
