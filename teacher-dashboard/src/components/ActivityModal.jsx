import React, { useState, useEffect } from 'react';
import { createActivity } from '../services/teacherApi';
import Button from './Button';
import { useToast } from './Toast';
import { PlusIcon, XIcon } from './Icons';

export default function ActivityModal({ isOpen, onClose, initialData }) {
  const toast = useToast();
  const [topic, setTopic] = useState('');
  const [subject, setSubject] = useState('Operating Systems');
  const [activityType, setActivityType] = useState('revision_practice');
  const [questionCount, setQuestionCount] = useState(5);
  const [difficulty, setDifficulty] = useState('adaptive');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (initialData) {
      setTopic(initialData.topic || 'Process Scheduling');
      setSubject(initialData.subject || 'Operating Systems');
    }
  }, [initialData]);

  if (!isOpen) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    const payload = {
      topic,
      subject,
      activity_type: activityType,
      target_student_ids: [],
      question_count: Number(questionCount),
      difficulty
    };

    try {
      await createActivity(payload);
      toast.success(`Revision activity created for ${topic}! (17 students notified)`);
      onClose();
    } catch (err) {
      toast.error('Failed to create revision activity. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="modal-overlay" onClick={() => !loading && onClose()}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2 className="modal-title" style={{ fontSize: '18px', fontWeight: 700 }}>
            Create Targeted Revision Activity
          </h2>
          <Button
            variant="ghost"
            size="sm"
            onClick={onClose}
            aria-label="Close modal"
            disabled={loading}
          >
            <XIcon size={16} />
          </Button>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Target Concept / Topic</label>
            <input
              type="text"
              className="form-control"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">Subject</label>
            <select
              className="form-control"
              value={subject}
              onChange={(e) => setSubject(e.target.value)}
            >
              <option value="Operating Systems">Operating Systems</option>
              <option value="Computer Networks">Computer Networks</option>
              <option value="DBMS">DBMS</option>
              <option value="Data Structures">Data Structures</option>
              <option value="Machine Learning">Machine Learning</option>
            </select>
          </div>

          <div className="form-group">
            <label className="form-label">Activity Type</label>
            <select
              className="form-control"
              value={activityType}
              onChange={(e) => setActivityType(e.target.value)}
            >
              <option value="revision_practice">Revision + Targeted Practice</option>
              <option value="quiz">Adaptive Check Quiz</option>
              <option value="homework">Review Assignment</option>
            </select>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
            <div className="form-group">
              <label className="form-label">Questions</label>
              <input
                type="number"
                className="form-control"
                value={questionCount}
                onChange={(e) => setQuestionCount(e.target.value)}
                min="1"
                max="15"
              />
            </div>

            <div className="form-group">
              <label className="form-label">Difficulty Level</label>
              <select
                className="form-control"
                value={difficulty}
                onChange={(e) => setDifficulty(e.target.value)}
              >
                <option value="adaptive">Adaptive (Recommended)</option>
                <option value="easy">Easy (Foundational)</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard (Challenge)</option>
              </select>
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px', marginTop: '20px' }}>
            <Button type="button" variant="secondary" size="md" onClick={onClose} disabled={loading}>
              Cancel
            </Button>
            <Button type="submit" variant="primary" size="md" loading={loading} icon={<PlusIcon size={16} />}>
              Create Activity
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
