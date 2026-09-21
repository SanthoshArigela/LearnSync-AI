import React from 'react';

export default function StatCard({ label, value, icon, footer, highlightColor }) {
  return (
    <div className="stat-card">
      <div className="stat-header">
        <span>{label}</span>
        <span style={{ fontSize: '20px' }}>{icon}</span>
      </div>
      <div className="stat-value" style={{ color: highlightColor || 'inherit' }}>
        {value}
      </div>
      {footer && <div className="stat-footer">{footer}</div>}
    </div>
  );
}
