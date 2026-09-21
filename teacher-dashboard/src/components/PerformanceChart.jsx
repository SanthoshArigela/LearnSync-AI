import React from 'react';

export default function PerformanceChart({ performances }) {
  if (!performances) return null;

  const getStatusClass = (score) => {
    if (score >= 80) return 'progress-strong';
    if (score >= 60) return 'progress-moderate';
    return 'progress-attention';
  };

  const getStatusLabel = (score) => {
    if (score >= 80) return 'Strong';
    if (score >= 60) return 'Moderate';
    return 'Needs Attention';
  };

  return (
    <div className="card-box">
      <h2 className="section-title">📊 Subject & Topic Performance Overview</h2>
      {Object.entries(performances).map(([subject, score]) => (
        <div key={subject} className="perf-item">
          <div className="perf-label">
            <span>{subject}</span>
            <span>
              {score}%{' '}
              <span
                style={{
                  fontSize: '12px',
                  fontWeight: 600,
                  marginLeft: '8px',
                  color: score < 60 ? '#D97706' : '#2563EB'
                }}
              >
                ({getStatusLabel(score)})
              </span>
            </span>
          </div>
          <div className="progress-track">
            <div
              className={`progress-fill ${getStatusClass(score)}`}
              style={{ width: `${score}%` }}
            ></div>
          </div>
        </div>
      ))}
    </div>
  );
}
