const BASE_URL = 'http://127.0.0.1:8000/api/teacher';

export async function fetchDashboard() {
  try {
    const res = await fetch(`${BASE_URL}/dashboard`);
    if (res.ok) return await res.json();
  } catch (e) {
    console.warn('Backend server unavailable, returning local fallback dashboard data:', e);
  }
  return {
    class_name: "B.Tech CSE — AI & ML",
    section: "Section A",
    total_students: 42,
    average_score: 78,
    students_needing_attention_count: 8,
    improving_students_count: 24,
    subject_performances: {
      "Computer Networks": 82,
      "Data Structures": 76,
      "DBMS": 71,
      "Operating Systems": 58,
      "Machine Learning": 64,
    },
    classroom_gaps: [
      {
        id: "topic_os_sched",
        topic: "Process Scheduling",
        subject: "Operating Systems",
        class_mastery: 58,
        affected_students_count: 17,
        severity: "HIGH",
        recommended_teaching_action: "Conduct a 10-minute revision on Round Robin & Priority Scheduling.",
        trend: "declining"
      },
      {
        id: "topic_tcp_term",
        topic: "TCP Connection Termination",
        subject: "Computer Networks",
        class_mastery: 54,
        affected_students_count: 14,
        severity: "HIGH",
        recommended_teaching_action: "Use a TCP 4-way FIN handshake sequence diagram.",
        trend: "declining"
      }
    ],
    misconceptions: [
      {
        id: "misc_os_1",
        topic: "Process Scheduling",
        subject: "Operating Systems",
        misconception_text: "Students are confusing waiting time with turnaround time in non-preemptive SJF.",
        affected_students_count: 14,
        recommended_resource: "Use a step-by-step Gantt chart timeline comparison before next quiz."
      },
      {
        id: "misc_tcp_1",
        topic: "TCP Connection Termination",
        subject: "Computer Networks",
        misconception_text: "Students are confusing SYN-ACK with final connection establishment.",
        affected_students_count: 12,
        recommended_resource: "Display an interactive TCP 4-way FIN state diagram during lecture."
      }
    ],
    students_needing_attention: [
      {
        student_id: "student_001",
        name: "Santhosh K.",
        overall_mastery: 52,
        weak_topic: "Process Scheduling",
        trend: "declining",
        recommended_action: "Assign Round Robin practice questions"
      },
      {
        student_id: "student_002",
        name: "Ananya Sharma",
        overall_mastery: 58,
        weak_topic: "DBMS Normalization",
        trend: "stable",
        recommended_action: "Review 3NF decomposition examples"
      }
    ],
    recommendations: [
      {
        id: "rec_t_1",
        priority: "HIGH",
        topic: "Process Scheduling",
        subject: "Operating Systems",
        affected_students_count: 17,
        why_evidence: "17 students scored below 60% mastery and 14 made repeated Gantt chart calculation mistakes.",
        recommended_action: "Conduct a 10-minute revision covering Round Robin time-quantum preemption rules.",
        expected_goal: "Improve class scheduling concept mastery from 58% to 75% before next quiz."
      }
    ]
  };
}

export async function fetchStudents() {
  try {
    const res = await fetch(`${BASE_URL}/students`);
    if (res.ok) return await res.json();
  } catch (e) {}
  const dash = await fetchDashboard();
  return dash.students_needing_attention || [];
}

export async function fetchStudentDetail(studentId) {
  try {
    const res = await fetch(`${BASE_URL}/students/${studentId}`);
    if (res.ok) return await res.json();
  } catch (e) {}
  return {
    student_id: studentId,
    name: "Santhosh K.",
    course: "B.Tech CSE — AI & ML (Section A)",
    overall_mastery: 52,
    recent_assessment_score: 48,
    trend: "declining",
    subject_masteries: {
      "Computer Networks": 82,
      "Data Structures": 76,
      "DBMS": 65,
      "Operating Systems": 48,
      "Machine Learning": 70,
    },
    weak_topics: ["Process Scheduling", "Threads & Memory"],
    recent_activities: [
      { type: "assessment", title: "Operating Systems Quiz 1", score: "45%", date: "2 hours ago" },
      { type: "tutor", title: "Asked AI Tutor about FIN handshake", date: "Yesterday" }
    ],
    recommended_action: "Assign a 10-minute targeted revision set on Process Scheduling."
  };
}

export async function fetchTopics() {
  try {
    const res = await fetch(`${BASE_URL}/topics`);
    if (res.ok) return await res.json();
  } catch (e) {}
  const dash = await fetchDashboard();
  return dash.classroom_gaps || [];
}

export async function fetchTopicDetail(topicId) {
  try {
    const res = await fetch(`${BASE_URL}/topics/${topicId}`);
    if (res.ok) return await res.json();
  } catch (e) {}
  return {
    id: topicId,
    topic: "Process Scheduling",
    subject: "Operating Systems",
    class_mastery: 58,
    affected_students_count: 17,
    severity: "HIGH",
    trend: "declining",
    mastery_distribution: { strong: 12, moderate: 13, needs_practice: 17 },
    struggling_students: ["Santhosh K.", "Vikram Singh", "Kavya Gupta"],
    common_mistakes: ["Students confuse waiting time with turnaround time in non-preemptive SJF."],
    recommended_teaching_action: "Conduct a 10-minute revision on Round Robin & Priority Scheduling."
  };
}

export async function fetchAssessments() {
  try {
    const res = await fetch(`${BASE_URL}/assessments`);
    if (res.ok) return await res.json();
  } catch (e) {}
  return [
    {
      id: "assess_1",
      title: "Operating Systems Midterm Quiz 1",
      subject: "Operating Systems",
      topic: "Process Scheduling",
      total_students: 42,
      average_score: 58,
      completion_rate: 95,
      most_difficult_question: "Calculate turnaround time for SJF with arrival times [0, 2, 4].",
      most_difficult_concept: "Gantt chart timeline calculation"
    }
  ];
}

export async function fetchRecommendations() {
  try {
    const res = await fetch(`${BASE_URL}/recommendations`);
    if (res.ok) return await res.json();
  } catch (e) {}
  const dash = await fetchDashboard();
  return dash.recommendations || [];
}

export async function createActivity(payload) {
  try {
    const res = await fetch(`${BASE_URL}/activities`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    if (res.ok) return await res.json();
  } catch (e) {}
  return {
    id: `act_${Date.now()}`,
    topic: payload.topic,
    subject: payload.subject || "Computer Science",
    activity_type: payload.activity_type || "revision_practice",
    target_student_ids: payload.target_student_ids || [],
    question_count: payload.question_count || 5,
    difficulty: payload.difficulty || "adaptive",
    status: "created",
    created_at: new Date().toISOString().slice(0, 16).replace('T', ' ')
  };
}

export async function resetDemoState() {
  try {
    const res = await fetch(`${BASE_URL}/demo/reset`, { method: 'POST' });
    if (res.ok) return await res.json();
  } catch (e) {}
  return { status: "success", message: "Demo state reset locally." };
}

