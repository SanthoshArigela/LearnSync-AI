import React from 'react';

export default function DashboardHeader({ title, subtitle, className = "B.Tech CSE — AI & ML", section = "A" }) {
  const currentDate = new Date().toLocaleDateString('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  });

  return (
    <div className="header-container">
      <div>
        <h1 className="header-title">{title || "Good afternoon, Teacher 👋"}</h1>
        <p className="header-subtitle">{subtitle || "Here's what your class needs today."}</p>
      </div>

      <div className="class-selector-group">
        <span className="class-badge">Class: {className}</span>
        <span className="class-badge">Sec: {section}</span>
        <span style={{ fontSize: '13px', color: '#64748B', marginLeft: '6px' }}>Updated: {currentDate}</span>
      </div>
    </div>
  );
}
