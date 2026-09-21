import React from 'react';
import Button from './Button';
import { PlusIcon, SearchIcon, BookOpenIcon } from './Icons';

export default function RecommendationCard({ rec, onCreateActivity, onViewStudents, onViewTopic }) {
  const priority = rec.priority || 'HIGH';

  return (
    <div
      style={{
        backgroundColor: '#FFFFFF',
        border: '1px solid #E2E8F0',
        borderRadius: '16px',
        padding: '20px',
        marginBottom: '16px',
        borderLeft: `6px solid ${priority === 'HIGH' ? '#EF4444' : priority === 'MEDIUM' ? '#F59E0B' : '#10B981'}`
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
        <div>
          <span className={`severity-tag ${priority}`}>{priority} Priority</span>
          <span style={{ marginLeft: '10px', fontSize: '13px', fontWeight: 600, color: '#64748B' }}>
            {rec.subject}
          </span>
        </div>
        <span style={{ fontSize: '13px', fontWeight: 700, color: '#4F46E5' }}>
          👥 {rec.affected_students_count} Students Affected
        </span>
      </div>

      <h3 style={{ fontSize: '18px', fontWeight: 700, color: '#0F172A', marginBottom: '8px' }}>
        WHAT: {rec.topic}
      </h3>

      <div style={{ fontSize: '14px', color: '#334155', marginBottom: '6px' }}>
        <strong>WHY (Evidence):</strong> {rec.why_evidence}
      </div>

      <div style={{ fontSize: '14px', color: '#0369A1', marginBottom: '6px' }}>
        <strong>ACTION:</strong> "{rec.recommended_action}"
      </div>

      {rec.expected_goal && (
        <div style={{ fontSize: '13px', color: '#15803D', marginBottom: '16px' }}>
          <strong>EXPECTED GOAL:</strong> {rec.expected_goal}
        </div>
      )}

      <div style={{ display: 'flex', gap: '10px', marginTop: '12px', flexWrap: 'wrap' }}>
        {onCreateActivity && (
          <Button
            variant="primary"
            size="md"
            icon={<PlusIcon size={16} />}
            onClick={() => onCreateActivity({ topic: rec.topic, subject: rec.subject })}
          >
            Create Revision Activity
          </Button>
        )}
        {onViewStudents && (
          <Button
            variant="secondary"
            size="md"
            icon={<SearchIcon size={16} />}
            onClick={() => onViewStudents(rec.topic)}
          >
            View Affected Students
          </Button>
        )}
        {onViewTopic && (
          <Button
            variant="secondary"
            size="md"
            icon={<BookOpenIcon size={16} />}
            onClick={() => onViewTopic(rec.topic)}
          >
            Inspect Topic
          </Button>
        )}
      </div>
    </div>
  );
}
