import React, { useState, useEffect } from 'react';
import DashboardHeader from '../components/DashboardHeader';
import RecommendationCard from '../components/RecommendationCard';
import ActivityModal from '../components/ActivityModal';
import { fetchRecommendations } from '../services/teacherApi';

export default function RecommendationsPage({ onNavigate }) {
  const [recommendations, setRecommendations] = useState([]);
  const [modalOpen, setModalOpen] = useState(false);
  const [modalData, setModalData] = useState(null);

  useEffect(() => {
    fetchRecommendations().then(setRecommendations);
  }, []);

  const handleCreateActivity = (data) => {
    setModalData(data);
    setModalOpen(true);
  };

  return (
    <div>
      <DashboardHeader
        title="AI Teacher Recommendations"
        subtitle="Explainable Teaching Strategies Powered by LearnSync AI Engine"
      />

      <div className="card-box" style={{ backgroundColor: '#EEF2FF', border: '1px solid #C7D2FE', marginBottom: '24px' }}>
        <h3 style={{ fontSize: '15px', fontWeight: 700, color: '#3730A3', marginBottom: '4px' }}>
          💡 AI Recommendation Architecture & Explainability (WHAT, WHO, WHY, ACTION)
        </h3>
        <p style={{ fontSize: '13.5px', color: '#4338CA', lineHeight: 1.5 }}>
          LearnSync AI analyzes student assessment responses, AI Tutor conversation topics, and mastery decay rates across Section A to generate deterministic, actionable teaching recommendations.
        </p>
      </div>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
        {recommendations.map((rec) => (
          <RecommendationCard
            key={rec.id}
            rec={rec}
            onCreateActivity={handleCreateActivity}
            onViewStudents={() => onNavigate('students')}
            onViewTopic={() => onNavigate('topics')}
          />
        ))}
      </div>

      <ActivityModal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        initialData={modalData}
      />
    </div>
  );
}
