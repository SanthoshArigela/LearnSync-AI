import React, { useState, useEffect } from 'react';
import DashboardHeader from '../components/DashboardHeader';
import StudentAttentionTable from '../components/StudentAttentionTable';
import ActivityModal from '../components/ActivityModal';
import { fetchStudents } from '../services/teacherApi';

export default function StudentsPage({ onNavigate }) {
  const [students, setStudents] = useState([]);
  const [search, setSearch] = useState('');
  const [modalOpen, setModalOpen] = useState(false);
  const [modalData, setModalData] = useState(null);

  useEffect(() => {
    fetchStudents().then(setStudents);
  }, []);

  const filtered = students.filter(s =>
    s.name.toLowerCase().includes(search.toLowerCase()) ||
    s.weak_topic.toLowerCase().includes(search.toLowerCase())
  );

  const handleOpenActivity = (data) => {
    setModalData(data);
    setModalOpen(true);
  };

  return (
    <div>
      <DashboardHeader title="Students Intelligence" subtitle="Class Roster & Individual Student Profiles" />

      <div className="card-box" style={{ marginBottom: '20px' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <input
            type="text"
            className="form-control"
            style={{ width: '300px' }}
            placeholder="Search students or weak topics..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <span style={{ fontSize: '13px', fontWeight: 600, color: '#64748B' }}>
            Showing {filtered.length} of 42 students
          </span>
        </div>
      </div>

      <StudentAttentionTable
        students={filtered}
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
