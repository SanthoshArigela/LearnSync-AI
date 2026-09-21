import React, { useState, useEffect } from 'react';
import DashboardHeader from '../components/DashboardHeader';
import ConnectionStatusHeader from '../components/ConnectionStatusHeader';
import LiveClassroomFeed from '../components/LiveClassroomFeed';
import StatCard from '../components/StatCard';
import PerformanceChart from '../components/PerformanceChart';
import TopicInsightCard from '../components/TopicInsightCard';
import MisconceptionCard from '../components/MisconceptionCard';
import StudentAttentionTable from '../components/StudentAttentionTable';
import RecommendationCard from '../components/RecommendationCard';
import ActivityModal from '../components/ActivityModal';
import { fetchDashboard } from '../services/teacherApi';

export default function DashboardPage({ onNavigate }) {
  const [data, setData] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [modalData, setModalData] = useState(null);

  // Real-time events & connection state
  const [events, setEvents] = useState([]);
  const [isConnected, setIsConnected] = useState(false);
  const [isRestFallback, setIsRestFallback] = useState(false);
  const [lastSync, setLastSync] = useState('Just now');

  useEffect(() => {
    fetchDashboard().then(setData);

    // Initial fetch of recent collaboration events
    fetch('http://127.0.0.1:8000/api/collaboration/events')
      .then((res) => res.ok ? res.json() : [])
      .then((evtData) => {
        if (evtData && evtData.length > 0) setEvents(evtData);
      })
      .catch(() => {});

    // Try WebSocket connection to FastAPI collaboration endpoint
    let ws = null;
    try {
      ws = new WebSocket('ws://127.0.0.1:8000/api/collaboration/ws/teacher/teacher_001');

      ws.onopen = () => {
        setIsConnected(true);
        setIsRestFallback(false);
        setLastSync(new Date().toLocaleTimeString());
      };

      ws.onmessage = (event) => {
        try {
          const newEvt = JSON.parse(event.data);
          setEvents((prev) => [newEvt, ...prev]);
          setLastSync(new Date().toLocaleTimeString());
        } catch (e) {}
      };

      ws.onerror = () => {
        setIsConnected(false);
        setIsRestFallback(true);
      };

      ws.onclose = () => {
        setIsConnected(false);
        setIsRestFallback(true);
      };
    } catch (e) {
      setIsConnected(false);
      setIsRestFallback(true);
    }

    // REST Polling fallback interval every 4 seconds if websocket is offline
    const interval = setInterval(() => {
      fetch('http://127.0.0.1:8000/api/collaboration/events?limit=20')
        .then((res) => res.ok ? res.json() : [])
        .then((evtData) => {
          if (evtData && evtData.length > 0) {
            setEvents(evtData);
            setLastSync(new Date().toLocaleTimeString());
            setIsRestFallback(true);
          }
        })
        .catch(() => {});
    }, 4000);

    return () => {
      if (ws) ws.close();
      clearInterval(interval);
    };
  }, []);

  const handleSimulateEvent = async () => {
    const demoEvt = {
      event_type: 'ASSESSMENT_COMPLETED',
      source: 'student',
      student_id: 'student_001',
      student_name: 'Santhosh K.',
      subject: 'Operating Systems',
      topic: 'Process Scheduling',
      subtopic: 'Round Robin Preemption',
      score: 58,
      mastery: 58,
      severity: 'HIGH',
      timestamp: new Date().toLocaleTimeString(),
      payload: { message: 'Completed targeted assessment on Student Web App' }
    };

    try {
      const res = await fetch('http://127.0.0.1:8000/api/collaboration/events', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(demoEvt)
      });
      if (res.ok) {
        const created = await res.json();
        setEvents((prev) => [created, ...prev]);
        setLastSync(new Date().toLocaleTimeString());
      }
    } catch (e) {
      setEvents((prev) => [demoEvt, ...prev]);
    }
  };

  if (!data) {
    return <div style={{ padding: '20px' }}>Loading classroom analytics...</div>;
  }

  const handleOpenActivity = (insight) => {
    setModalData(insight);
    setModalOpen(true);
  };

  return (
    <div>
      <DashboardHeader
        title="Good afternoon, Teacher 👋"
        subtitle="Here's what your class needs today."
        className={data.class_name}
        section={data.section}
      />

      {/* Connection Status & Live Office Kit Sync Bar */}
      <ConnectionStatusHeader
        isConnected={isConnected}
        isRestFallback={isRestFallback}
        lastSync={lastSync}
        onTriggerDemoEvent={handleSimulateEvent}
      />

      {/* Summary Cards */}
      <div className="stats-grid">
        <StatCard label="Total Students" value={`${data.total_students} Students`} icon="👥" footer="Enrolled in Section A" />
        <StatCard label="Average Class Score" value={`${data.average_score}%`} icon="⭐" highlightColor="#2563EB" footer="Across 5 active subjects" />
        <StatCard label="Students Needing Attention" value={`${data.students_needing_attention_count} Students`} icon="⚠️" highlightColor="#DC2626" footer="Mastery below 60%" />
        <StatCard label="Improving Students" value={`${data.improving_students_count} Students`} icon="📈" highlightColor="#166534" footer="+8% this semester" />
      </div>

      {/* Live Classroom Feed & Learning Gaps */}
      <div className="grid-2col">
        <LiveClassroomFeed
          events={events}
          onSelectStudent={(id) => onNavigate('student-detail', id)}
          onViewTopic={(topicId) => onNavigate('topic-detail', topicId)}
        />

        <div>
          <h2 className="section-title">⚠️ Classroom Learning Gaps</h2>
          {data.classroom_gaps && data.classroom_gaps.map((gap) => (
            <TopicInsightCard
              key={gap.id}
              gap={gap}
              onCreateActivity={handleOpenActivity}
              onViewTopic={(topicId) => onNavigate('topic-detail', topicId)}
            />
          ))}
        </div>
      </div>

      {/* Common Misconceptions */}
      <h2 className="section-title">💡 Common Misconceptions (AI Extracted)</h2>
      <div className="grid-2col" style={{ marginBottom: '32px' }}>
        {data.misconceptions && data.misconceptions.map((item) => (
          <MisconceptionCard key={item.id} item={item} />
        ))}
      </div>

      {/* Subject & Topic Performance */}
      <PerformanceChart performances={data.subject_performances} />

      {/* AI Teacher Recommendations (Explainable) */}
      <h2 className="section-title">🤖 AI Teaching Recommendations</h2>
      {data.recommendations && data.recommendations.map((rec) => (
        <RecommendationCard
          key={rec.id}
          rec={rec}
          onCreateActivity={handleOpenActivity}
          onViewStudents={() => onNavigate('students')}
          onViewTopic={() => onNavigate('topics')}
        />
      ))}

      {/* Students Needing Attention */}
      <StudentAttentionTable
        students={data.students_needing_attention}
        onSelectStudent={(id) => onNavigate('student-detail', id)}
        onCreateActivity={handleOpenActivity}
      />

      <ActivityModal
        isOpen={modalOpen}
        onClose={() => setModalOpen(false)}
        initialData={modalData}
      />
    </div>
  );
}
