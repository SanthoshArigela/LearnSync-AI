import React, { useState, useEffect } from 'react';
import SidebarNav from './components/SidebarNav';
import DashboardPage from './pages/DashboardPage';
import StudentsPage from './pages/StudentsPage';
import StudentDetailPage from './pages/StudentDetailPage';
import TopicsPage from './pages/TopicsPage';
import TopicDetailPage from './pages/TopicDetailPage';
import AssessmentsPage from './pages/AssessmentsPage';
import RecommendationsPage from './pages/RecommendationsPage';
import ProfilePage from './pages/ProfilePage';
import LoginPage from './pages/LoginPage';
import StudentWebAppView from './components/StudentWebAppView';
import { ToastProvider } from './components/Toast';
import { authService } from './services/authService';

export default function App() {
  const [session, setSession] = useState(() => authService.getSession());
  const [activeTab, setActiveTab] = useState('dashboard');
  const [selectedStudentId, setSelectedStudentId] = useState(null);
  const [selectedTopicId, setSelectedTopicId] = useState(null);

  // Sync hash routing & protection
  useEffect(() => {
    const handleHashChange = () => {
      const hash = window.location.hash || '';
      const currentSession = authService.getSession();
      setSession(currentSession);

      if (!currentSession || !currentSession.authenticated) {
        if (hash !== '#/login') {
          window.location.hash = '/login';
        }
        return;
      }

      const role = currentSession.user.role;

      // Role Protection Rules
      if (role === 'student') {
        if (hash.startsWith('#/faculty') || hash === '#/login' || hash === '') {
          window.location.hash = '/student/home';
        }
      } else if (role === 'faculty') {
        if (hash.startsWith('#/student') || hash === '#/login' || hash === '') {
          window.location.hash = '/faculty/dashboard';
        } else if (hash.startsWith('#/faculty/')) {
          const tab = hash.replace('#/faculty/', '');
          if (['dashboard', 'students', 'topics', 'assessments', 'recommendations', 'profile'].includes(tab)) {
            setActiveTab(tab);
          }
        }
      }
    };

    handleHashChange();
    window.addEventListener('hashchange', handleHashChange);
    return () => window.removeEventListener('hashchange', handleHashChange);
  }, [session?.authenticated, session?.user?.role]);

  const handleLoginSuccess = (user) => {
    const newSession = authService.getSession();
    setSession(newSession);
    if (user.role === 'student') {
      window.location.hash = '/student/home';
    } else {
      window.location.hash = '/faculty/dashboard';
      setActiveTab('dashboard');
    }
  };

  const handleLogout = () => {
    authService.logout();
    setSession(null);
    window.location.hash = '/login';
  };

  const handleNavigate = (tab, payload = null) => {
    if (tab === 'student-detail') {
      setSelectedStudentId(payload || 'student_001');
      setActiveTab('student-detail');
    } else if (tab === 'topic-detail') {
      setSelectedTopicId(payload || 'topic_os_sched');
      setActiveTab('topic-detail');
    } else {
      setActiveTab(tab);
      window.location.hash = `/faculty/${tab}`;
    }
    window.scrollTo(0, 0);
  };

  // Content render helper
  const renderContent = () => {
    // 1. Unauthenticated Route Protection -> /login
    if (!session || !session.authenticated) {
      return <LoginPage onLoginSuccess={handleLoginSuccess} />;
    }

    // 2. Student Role Experience -> Student Web App
    if (session.user.role === 'student') {
      return <StudentWebAppView user={session.user} onLogout={handleLogout} />;
    }

    // 3. Faculty Role Experience -> Faculty Web Dashboard
    const renderFacultyContent = () => {
      switch (activeTab) {
        case 'dashboard':
          return <DashboardPage onNavigate={handleNavigate} />;
        case 'students':
          return <StudentsPage onNavigate={handleNavigate} />;
        case 'student-detail':
          return <StudentDetailPage studentId={selectedStudentId} onNavigate={handleNavigate} />;
        case 'topics':
          return <TopicsPage onNavigate={handleNavigate} />;
        case 'topic-detail':
          return <TopicDetailPage topicId={selectedTopicId} onNavigate={handleNavigate} />;
        case 'assessments':
          return <AssessmentsPage onNavigate={handleNavigate} />;
        case 'recommendations':
          return <RecommendationsPage onNavigate={handleNavigate} />;
        case 'profile':
          return <ProfilePage onLogout={handleLogout} />;
        default:
          return <DashboardPage onNavigate={handleNavigate} />;
      }
    };

    return (
      <div className="app-layout">
        <SidebarNav activeTab={activeTab} setActiveTab={setActiveTab} onLogout={handleLogout} />
        <main className="main-content">
          {renderFacultyContent()}
        </main>
      </div>
    );
  };

  return (
    <ToastProvider>
      {renderContent()}
    </ToastProvider>
  );
}
