import React from 'react';
import Button from './Button';
import { PlusIcon, SearchIcon } from './Icons';

export default function TopicInsightCard({ gap, onCreateActivity, onViewTopic }) {
  const severity = gap.severity || 'HIGH';

  return (
    <div className={`insight-card ${severity}`}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div className="insight-topic">⚠ {gap.topic}</div>
        <span className={`severity-tag ${severity}`}>{severity} Priority</span>
      </div>

      <div className="insight-meta">
        <span>Subject: {gap.subject}</span>
        <span>•</span>
        <span>Class Mastery: {gap.class_mastery}%</span>
        <span>•</span>
        <span>Affected: {gap.affected_students_count} Students</span>
      </div>

      <p style={{ fontSize: '13.5px', color: '#475569', margin: '8px 0 12px 0' }}>
        <strong>Recommended Action:</strong> "{gap.recommended_teaching_action}"
      </p>

      <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
        {onCreateActivity && (
          <Button
            variant="primary"
            size="sm"
            icon={<PlusIcon size={14} />}
            onClick={() => onCreateActivity(gap)}
          >
            Create Revision Activity
          </Button>
        )}
        {onViewTopic && (
          <Button
            variant="secondary"
            size="sm"
            icon={<SearchIcon size={14} />}
            onClick={() => onViewTopic(gap.id)}
          >
            Inspect Topic
          </Button>
        )}
      </div>
    </div>
  );
}
