import React, { useState, useRef, useEffect } from 'react';
import { authService } from '../services/authService';
import Button from './Button';
import { useToast } from './Toast';
import ErrorBoundary from './ErrorBoundary';
import {
  LogoutIcon,
  SparklesIcon,
  CameraIcon,
  MicIcon,
  SendIcon,
  UploadIcon,
  RefreshIcon,
  CheckIcon,
  StopIcon,
  PlayIcon,
  BookOpenIcon,
  CheckCircleIcon,
  AlertCircleIcon,
  InfoIcon
} from './Icons';

export default function StudentWebAppView({ user, onLogout }) {
  const toast = useToast();
  const [activeTab, setActiveTab] = useState('home');
  const [tutorMode, setTutorMode] = useState('simple');
  const [tutorQuery, setTutorQuery] = useState('');
  const [conversationId] = useState(() => `student_conv_${Date.now()}_${Math.random().toString(36).substring(2, 7)}`);
  const [tutorMessages, setTutorMessages] = useState([
    {
      role: 'assistant',
      text: '### Concept Summary\nHello Santhosh! I am your LearnSync AI Tutor.\n\n### Simple Explanation\nAsk me anything about C Programming, Data Structures, Java, Python, Computer Networks, DBMS, or Operating Systems!',
      followups: ['Fundamentals in C', 'Explain TCP three-way handshake', 'What is a binary search tree?']
    }
  ]);
  const [isAsking, setIsAsking] = useState(false);

  // Vision AI State
  const fileInputRef = useRef(null);
  const [visionFile, setVisionFile] = useState(null);
  const [visionPreview, setVisionPreview] = useState(null);
  const [visionFileName, setVisionFileName] = useState('');
  const [visionFileSize, setVisionFileSize] = useState('');
  const [isAnalyzingVision, setIsAnalyzingVision] = useState(false);
  const [visionResult, setVisionResult] = useState(null);

  // Voice AI State
  const [isListeningVoice, setIsListeningVoice] = useState(false);
  const [voiceState, setVoiceState] = useState('idle'); // idle | listening | transcribing | processing | completed | error
  const [voiceTranscript, setVoiceTranscript] = useState('');
  const voiceTranscriptRef = useRef('');
  const [voiceAiResponse, setVoiceAiResponse] = useState('');
  const [voiceFollowups, setVoiceFollowups] = useState([]);
  const [recognitionInstance, setRecognitionInstance] = useState(null);
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);

  // Adaptive Assessment State
  const [assessmentLoading, setAssessmentLoading] = useState(false);
  const [activeAssessment, setActiveAssessment] = useState(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [assessmentSubmitted, setAssessmentSubmitted] = useState(false);
  const [assessmentResult, setAssessmentResult] = useState(null);
  const [evaluatingAssessment, setEvaluatingAssessment] = useState(false);

  // Time-based greeting helper
  const getGreeting = () => {
    const hour = new Date().getHours();
    const name = user?.name || 'Santhosh';
    if (hour < 12) return `Good morning, ${name} 👋`;
    if (hour < 17) return `Good afternoon, ${name} 👋`;
    return `Good evening, ${name} 👋`;
  };

  // AI Tutor submit
  const handleAskTutor = async (e, customQuery = null) => {
    if (e) e.preventDefault();
    const queryToUse = customQuery || tutorQuery;
    if (!queryToUse.trim()) return;

    const userText = queryToUse.trim();
    setTutorMessages(prev => [...prev, { role: 'user', text: userText }]);
    if (!customQuery) setTutorQuery('');
    setIsAsking(true);

    try {
      const response = await fetch('/api/tutor/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: userText,
          explanation_mode: tutorMode,
          conversation_id: conversationId
        }),
      });
      if (response.ok) {
        const data = await response.json();
        setTutorMessages(prev => [
          ...prev,
          {
            role: 'assistant',
            text: data.answer || 'Solution generated.',
            suggested_followups: data.suggested_followups || [],
            quiz: data.quiz || null
          }
        ]);
        if (data.quiz) {
          toast.success('AI Tutor attached a follow-up practice quiz question below!');
        }
        toast.success("AI response received.");
      } else {
        toast.error("Failed to reach AI Tutor. Please try again.");
      }
    } catch (err) {
      toast.error("LearnSync AI is temporarily unable to process the request. Please check connection and try again.");
    } finally {
      setIsAsking(false);
    }
  };

  // ----------------------------------------------------
  // VISION AI HANDLERS
  // ----------------------------------------------------
  const handleSelectImageClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  const handleVisionFileChange = (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    // File validation
    const validTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/webp'];
    if (!validTypes.includes(file.type)) {
      toast.error('Invalid image format. Please select a PNG, JPG, JPEG, or WEBP image.');
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      toast.error('Image file is too large (max 5MB allowed).');
      return;
    }

    const reader = new FileReader();
    reader.onload = () => {
      setVisionFile(file);
      setVisionPreview(reader.result);
      setVisionFileName(file.name);
      setVisionFileSize((file.size / 1024).toFixed(1) + ' KB');
      setVisionResult(null);
      toast.info('Image loaded — click "Analyze & Solve Problem" to continue.');
    };
    reader.readAsDataURL(file);
  };

  const handleAnalyzeVision = async () => {
    if (!visionPreview) {
      toast.warning('Please select an image file first.');
      return;
    }

    setIsAnalyzingVision(true);
    toast.info('Vision AI Scanner processing problem image…');

    try {
      const response = await fetch('/api/vision/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          image_base64: visionPreview
        })
      });

      if (response.ok) {
        const data = await response.json();
        setVisionResult(data.extracted);
        toast.success('Vision AI extracted and solved the problem statement!');
      } else {
        toast.error('Vision AI failed to analyze image. Please try again.');
      }
    } catch (err) {
      toast.error('Network error during Vision AI processing.');
    } finally {
      setIsAnalyzingVision(false);
    }
  };

  const handleClearVision = () => {
    setVisionFile(null);
    setVisionPreview(null);
    setVisionFileName('');
    setVisionFileSize('');
    setVisionResult(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  // ----------------------------------------------------
  // VOICE AI HANDLERS
  // ----------------------------------------------------
  const processVoiceQuery = async (queryText) => {
    if (!queryText || !queryText.trim()) {
      toast.warning('No speech detected. Please speak or type your question.');
      setVoiceState('idle');
      return;
    }

    setVoiceState('processing');
    toast.info('Transcribing & processing spoken question with Gemini AI...');

    try {
      const res = await fetch('/api/tutor/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: queryText.trim(),
          explanation_mode: 'simple',
          conversation_id: conversationId
        })
      });

      if (res.ok) {
        const data = await res.json();
        setVoiceAiResponse(data.answer);
        setVoiceFollowups(data.suggested_followups || []);
        setVoiceState('completed');
        toast.success('Voice AI response ready!');
      } else {
        toast.error('Failed to get Voice AI response.');
        setVoiceState('error');
      }
    } catch (err) {
      toast.error('Network error during Voice AI processing.');
      setVoiceState('error');
    }
  };

  useEffect(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (SpeechRecognition) {
      const recog = new SpeechRecognition();
      recog.continuous = false;
      recog.interimResults = true;
      recog.lang = 'en-US';

      recog.onstart = () => {
        setIsListeningVoice(true);
        setVoiceState('listening');
        toast.success('Listening… speak your doubt clearly.');
      };

      recog.onresult = (event) => {
        let transcript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          transcript += event.results[i][0].transcript;
        }
        setVoiceTranscript(transcript);
        voiceTranscriptRef.current = transcript;
      };

      recog.onerror = (event) => {
        setIsListeningVoice(false);
        setVoiceState('error');
        if (event.error === 'not-allowed') {
          toast.error('Microphone permission denied. Please allow microphone access in browser settings.');
        } else {
          toast.error(`Speech recognition error: ${event.error}`);
        }
      };

      recog.onend = () => {
        setIsListeningVoice(false);
        const finalCaptured = (voiceTranscriptRef.current || '').trim();
        if (finalCaptured) {
          processVoiceQuery(finalCaptured);
        }
      };

      setRecognitionInstance(recog);
    }
  }, []);

  const handleStartListening = () => {
    voiceTranscriptRef.current = '';
    setVoiceTranscript('');
    setVoiceAiResponse('');
    setVoiceState('listening');
    if (recognitionInstance) {
      try {
        recognitionInstance.start();
      } catch (err) {
        toast.warning('Microphone session active. Speak your question.');
      }
    } else {
      toast.warning('Browser speech recognition not supported. You can type your voice doubt below.');
    }
  };

  const handleStopListening = async () => {
    if (recognitionInstance && isListeningVoice) {
      recognitionInstance.stop();
    }
    setIsListeningVoice(false);
    const captured = (voiceTranscriptRef.current || voiceTranscript).trim();
    if (captured) {
      processVoiceQuery(captured);
    } else {
      toast.warning('No speech detected. Please speak or type your question.');
      setVoiceState('idle');
    }
  };

  const handleReadAloud = (text) => {
    if (!('speechSynthesis' in window)) {
      toast.warning('Text-to-speech audio playback is not supported in this browser.');
      return;
    }

    if (isPlayingAudio) {
      window.speechSynthesis.cancel();
      setIsPlayingAudio(false);
      return;
    }

    // Clean markdown headings/symbols for speech
    const cleanText = text.replace(/###/g, '').replace(/\*\*/g, '').replace(/```[\s\S]*?```/g, 'Code example included in text.');
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.onend = () => setIsPlayingAudio(false);
    utterance.onerror = () => setIsPlayingAudio(false);

    setIsPlayingAudio(true);
    window.speechSynthesis.speak(utterance);
    toast.info('Playing AI response audio...');
  };

  // ----------------------------------------------------
  // ADAPTIVE ASSESSMENT HANDLERS
  // ----------------------------------------------------
  const handleStartAssessment = async () => {
    setAssessmentLoading(true);
    toast.info('Preparing your adaptive assessment challenge...');

    try {
      const res = await fetch('/api/assessment/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          subject: 'Computer Networks',
          topic: 'TCP',
          difficulty: 'adaptive',
          question_count: 5
        })
      });

      if (res.ok) {
        const data = await res.json();
        setActiveAssessment(data);
        setCurrentQuestionIndex(0);
        setSelectedAnswers({});
        setAssessmentSubmitted(false);
        setAssessmentResult(null);
        toast.success('Adaptive assessment loaded! Good luck.');
      } else {
        toast.error('Failed to generate assessment. Please try again.');
      }
    } catch (err) {
      toast.error('Network error generating adaptive assessment.');
    } finally {
      setAssessmentLoading(false);
    }
  };

  const handleSelectOption = (qId, optionKey) => {
    if (assessmentSubmitted) return;
    setSelectedAnswers(prev => ({ ...prev, [qId]: optionKey }));
  };

  const handleSubmitAssessment = async () => {
    if (!activeAssessment) return;

    const unanswered = activeAssessment.questions.filter(q => !selectedAnswers[q.id]);
    if (unanswered.length > 0) {
      toast.warning(`Please answer all ${activeAssessment.questions.length} questions before submitting.`);
      return;
    }

    setEvaluatingAssessment(true);
    toast.info('Evaluating answers and computing mastery score…');

    const submissions = activeAssessment.questions.map(q => ({
      question_id: q.id,
      selected_key: selectedAnswers[q.id],
      question_text: q.question,
      correct_key: q.correct_key,
      topic: q.topic,
      explanation: q.explanation
    }));

    try {
      const res = await fetch('/api/assessment/evaluate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          assessment_id: activeAssessment.assessment_id,
          subject: activeAssessment.subject,
          topic: activeAssessment.topic,
          difficulty: activeAssessment.requested_difficulty,
          submissions
        })
      });

      if (res.ok) {
        const result = await res.json();
        setAssessmentResult(result);
        setAssessmentSubmitted(true);
        toast.success(`Assessment submitted! Score: ${result.score}/${result.total} (${result.percentage}%)`);
      } else {
        toast.error('Failed to evaluate assessment.');
      }
    } catch (err) {
      toast.error('Error submitting assessment evaluation.');
    } finally {
      setEvaluatingAssessment(false);
    }
  };

  // ----------------------------------------------------
  // MARKDOWN RENDERER
  // ----------------------------------------------------
  const renderFormattedTutorText = (text) => {
    if (!text) return null;
    const lines = text.split('\n');
    let inCodeBlock = false;
    let codeBuffer = [];
    const elements = [];

    lines.forEach((line, idx) => {
      const trimmed = line.trim();

      if (trimmed.startsWith('```')) {
        if (inCodeBlock) {
          elements.push(
            <pre key={`code-${idx}`} style={{
              backgroundColor: '#1E293B',
              color: '#38BDF8',
              padding: '12px 16px',
              borderRadius: '10px',
              fontSize: '13px',
              fontFamily: 'Consolas, Monaco, monospace',
              overflowX: 'auto',
              margin: '8px 0',
              border: '1px solid #334155'
            }}>
              <code>{codeBuffer.join('\n')}</code>
            </pre>
          );
          codeBuffer = [];
          inCodeBlock = false;
        } else {
          inCodeBlock = true;
        }
        return;
      }

      if (inCodeBlock) {
        codeBuffer.push(line);
        return;
      }

      if (!trimmed) {
        elements.push(<div key={`blank-${idx}`} style={{ height: '6px' }} />);
        return;
      }

      if (trimmed.startsWith('### ')) {
        const title = trimmed.replace(/^###\s+/, '');
        elements.push(
          <div key={`head-${idx}`} style={{
            color: '#4F46E5',
            fontSize: '15px',
            fontWeight: 800,
            marginTop: '12px',
            marginBottom: '4px',
            display: 'flex',
            alignItems: 'center',
            gap: '6px'
          }}>
            <span style={{ width: '4px', height: '14px', backgroundColor: '#4F46E5', borderRadius: '2px', display: 'inline-block' }}></span>
            <span>{title}</span>
          </div>
        );
        return;
      }

      const formattedParts = trimmed.split(/(\*\*.*?\*\*)/g).map((chunk, j) => {
        if (chunk.startsWith('**') && chunk.endsWith('**')) {
          return <strong key={j} style={{ color: '#0F172A', fontWeight: 700 }}>{chunk.slice(2, -2)}</strong>;
        }
        return chunk;
      });

      elements.push(
        <div key={`line-${idx}`} style={{ fontSize: '14px', lineHeight: 1.6, color: '#334155' }}>
          {formattedParts}
        </div>
      );
    });

    return <div>{elements}</div>;
  };

  // ----------------------------------------------------
  // RENDER TABS
  // ----------------------------------------------------
  const renderTabContent = () => {
    switch (activeTab) {
      case 'home':
        return (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
            <div className="card-box" style={{ background: 'linear-gradient(135deg, #4F46E5 0%, #3730A3 100%)', color: '#FFFFFF' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '12px' }}>
                <div>
                  <h1 style={{ fontSize: '24px', fontWeight: 800, margin: 0, color: '#FFFFFF' }}>
                    {getGreeting()}
                  </h1>
                  <p style={{ fontSize: '14px', color: '#E0E7FF', marginTop: '6px', margin: 0 }}>
                    Ready to continue learning Computer Networks & Operating Systems?
                  </p>
                </div>
                <span style={{ backgroundColor: 'rgba(255,255,255,0.2)', padding: '6px 12px', borderRadius: '20px', fontSize: '12px', fontWeight: 700 }}>
                  B.Tech CSE (Sec A)
                </span>
              </div>
            </div>

            <div className="card-box">
              <h2 className="section-title">🤖 Ask LearnSync AI Tutor</h2>
              <p style={{ color: '#64748B', fontSize: '14px', marginBottom: '16px' }}>
                Instant explanations with Simple, Real-World, and Technical modes.
              </p>
              <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
                <Button variant="primary" size="md" icon={<SparklesIcon size={16} />} onClick={() => setActiveTab('tutor')} style={{ flex: 1 }}>
                  Open AI Tutor Chat
                </Button>
                <Button variant="secondary" size="md" icon={<CameraIcon size={16} />} onClick={() => setActiveTab('vision')} style={{ flex: 1 }}>
                  Scan Question (Vision AI)
                </Button>
                <Button variant="secondary" size="md" icon={<MicIcon size={16} />} onClick={() => setActiveTab('voice')} style={{ flex: 1 }}>
                  Ask by Voice
                </Button>
              </div>
            </div>

            <div className="grid-2col">
              <div className="card-box">
                <h2 className="section-title">📊 Today's Progress</h2>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', fontSize: '14px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span style={{ color: '#64748B' }}>Learning Time</span>
                    <strong>42 min</strong>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span style={{ color: '#64748B' }}>Questions Solved</span>
                    <strong>8 Questions</strong>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                    <span style={{ color: '#64748B' }}>Average Quiz Score</span>
                    <strong style={{ color: '#16A34A' }}>82%</strong>
                  </div>
                </div>
              </div>

              <div className="card-box" style={{ borderLeft: '4px solid #4F46E5' }}>
                <h2 className="section-title">💡 Recommended for You</h2>
                <h3 style={{ fontSize: '15px', fontWeight: 700, margin: '4px 0 6px 0', color: '#0F172A' }}>
                  Revise OSI Model & TCP Handshake
                </h3>
                <p style={{ fontSize: '13px', color: '#64748B', margin: '0 0 14px 0' }}>
                  Identified minor hesitation on Layer 4 transport protocols during practice.
                </p>
                <Button variant="primary" size="sm" icon={<CheckIcon size={14} />} onClick={() => setActiveTab('assessments')}>
                  Start Targeted Quiz
                </Button>
              </div>
            </div>
          </div>
        );

      case 'tutor':
        return (
          <div className="card-box" style={{ display: 'flex', flexDirection: 'column', height: '640px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', borderBottom: '1px solid #E2E8F0', paddingBottom: '12px', flexWrap: 'wrap', gap: '8px' }}>
              <h2 className="section-title" style={{ margin: 0 }}>🤖 LearnSync AI Tutor</h2>
              <div style={{ display: 'flex', gap: '6px' }}>
                {['simple', 'real-world', 'technical'].map((mode) => (
                  <Button
                    key={mode}
                    variant={tutorMode === mode ? 'primary' : 'ghost'}
                    size="sm"
                    onClick={() => setTutorMode(mode)}
                    style={{ textTransform: 'capitalize' }}
                  >
                    {mode}
                  </Button>
                ))}
              </div>
            </div>

            <div style={{ flex: 1, overflowY: 'auto', paddingRight: '8px', display: 'flex', flexDirection: 'column', gap: '14px' }}>
              {tutorMessages.map((msg, idx) => (
                <div key={idx} style={{ display: 'flex', flexDirection: 'column', alignItems: msg.role === 'user' ? 'flex-end' : 'flex-start' }}>
                  <div
                    style={{
                      maxWidth: '85%',
                      backgroundColor: msg.role === 'user' ? '#4F46E5' : '#FFFFFF',
                      color: msg.role === 'user' ? '#FFFFFF' : '#0F172A',
                      padding: '14px 18px',
                      borderRadius: '16px',
                      border: msg.role === 'user' ? 'none' : '1px solid #E2E8F0',
                      boxShadow: msg.role === 'user' ? '0 4px 12px rgba(79,70,229,0.2)' : '0 2px 8px rgba(0,0,0,0.04)'
                    }}
                  >
                    {msg.role === 'user' ? msg.text : renderFormattedTutorText(msg.text)}
                  </div>

                  {msg.role === 'assistant' && msg.followups && msg.followups.length > 0 && (
                    <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap', marginTop: '8px', maxWidth: '85%' }}>
                      {msg.followups.map((chip, cIdx) => (
                        <button
                          key={cIdx}
                          onClick={() => handleAskTutor(null, chip)}
                          style={{
                            padding: '6px 12px',
                            borderRadius: '16px',
                            backgroundColor: '#EEF2FF',
                            border: '1px solid #C7D2FE',
                            color: '#3730A3',
                            fontSize: '12px',
                            fontWeight: 600,
                            cursor: 'pointer'
                          }}
                        >
                          💡 {chip}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              ))}
              {isAsking && <div style={{ color: '#64748B', fontSize: '13px', fontStyle: 'italic' }}>LearnSync AI is analyzing question...</div>}
            </div>

            <form onSubmit={handleAskTutor} style={{ display: 'flex', gap: '10px', marginTop: '16px', paddingTop: '12px', borderTop: '1px solid #E2E8F0' }}>
              <input
                type="text"
                value={tutorQuery}
                onChange={(e) => setTutorQuery(e.target.value)}
                placeholder="Ask a question (e.g. fundamentals in c)..."
                style={{ flex: 1, padding: '12px 16px', borderRadius: '10px', border: '1px solid #CBD5E1', outline: 'none', fontSize: '14px' }}
              />
              <Button type="submit" loading={isAsking} variant="primary" size="md" icon={<SendIcon size={16} />}>
                Send
              </Button>
            </form>
          </div>
        );

      case 'vision':
        return (
          <ErrorBoundary
            title="Vision AI encountered an unexpected error."
            message="Please try selecting another image or resetting the view."
            onReset={handleClearVision}
          >
            <div className="card-box">
              <h2 className="section-title">📷 Vision AI Problem Solver</h2>
              <p style={{ color: '#64748B', fontSize: '14px', marginBottom: '20px' }}>
                Upload or scan a diagram/homework question to get an instant step-by-step AI solution.
              </p>

              <input
                type="file"
                ref={fileInputRef}
                style={{ display: 'none' }}
                accept="image/png,image/jpeg,image/jpg,image/webp"
                onChange={handleVisionFileChange}
              />

              {!visionPreview ? (
                <div
                  style={{
                    border: '2px dashed #CBD5E1',
                    borderRadius: '16px',
                    padding: '40px 20px',
                    textAlign: 'center',
                    backgroundColor: '#F8FAFC',
                    cursor: 'pointer'
                  }}
                  onClick={handleSelectImageClick}
                >
                  <div style={{ fontSize: '40px', marginBottom: '12px' }}>📷</div>
                  <div style={{ fontSize: '16px', fontWeight: 700, color: '#0F172A' }}>Drop your problem image here or click to browse</div>
                  <div style={{ fontSize: '13px', color: '#64748B', marginTop: '4px', marginBottom: '20px' }}>
                    Supports PNG, JPG, JPEG, WEBP (Max 5MB)
                  </div>
                  <Button
                    variant="primary"
                    size="md"
                    icon={<UploadIcon size={16} />}
                    onClick={(e) => { e.stopPropagation(); handleSelectImageClick(); }}
                  >
                    Select Image File
                  </Button>
                </div>
              ) : (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                  <div style={{ display: 'flex', gap: '20px', alignItems: 'center', padding: '16px', backgroundColor: '#F8FAFC', borderRadius: '14px', border: '1px solid #E2E8F0', flexWrap: 'wrap' }}>
                    <img
                      src={visionPreview}
                      alt="Problem Preview"
                      style={{ width: '120px', height: '120px', objectFit: 'cover', borderRadius: '10px', border: '1px solid #CBD5E1' }}
                    />
                    <div style={{ flex: 1 }}>
                      <div style={{ fontSize: '15px', fontWeight: 700, color: '#0F172A' }}>{visionFileName || 'Uploaded Image'}</div>
                      <div style={{ fontSize: '13px', color: '#64748B', marginTop: '4px' }}>File Size: {visionFileSize || 'Ready'}</div>
                      <div style={{ display: 'flex', gap: '10px', marginTop: '14px' }}>
                        <Button
                          variant="primary"
                          size="md"
                          loading={isAnalyzingVision}
                          icon={<SparklesIcon size={16} />}
                          onClick={handleAnalyzeVision}
                        >
                          Analyze & Solve Problem
                        </Button>
                        <Button
                          variant="secondary"
                          size="md"
                          disabled={isAnalyzingVision}
                          onClick={handleClearVision}
                        >
                          Select Different Image
                        </Button>
                      </div>
                    </div>
                  </div>

                  {visionResult && (
                    <div style={{ padding: '20px', backgroundColor: '#F0FDF4', borderRadius: '14px', border: '1px solid #86EFAC' }}>
                      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                        <span style={{ fontSize: '14px', fontWeight: 700, color: '#166534', display: 'flex', alignItems: 'center', gap: '6px' }}>
                          <CheckCircleIcon size={18} /> Extracted Problem Statement
                        </span>
                        <span style={{ fontSize: '12px', fontWeight: 600, backgroundColor: '#DCFCE7', color: '#14532D', padding: '3px 8px', borderRadius: '6px' }}>
                          {visionResult.topic || 'Computer Science'} • Confidence: {visionResult.confidence != null ? (visionResult.confidence * 100).toFixed(0) : '95'}%
                        </span>
                      </div>

                      <div style={{ fontSize: '16px', fontWeight: 700, color: '#0F172A', marginBottom: '12px', backgroundColor: '#FFFFFF', padding: '14px', borderRadius: '10px', border: '1px solid #CBD5E1' }}>
                        {visionResult.question || 'Problem statement extracted'}
                      </div>

                      {visionResult.raw_ocr_text && (
                        <div style={{ fontSize: '13px', color: '#475569', marginTop: '10px' }}>
                          <strong>OCR Raw Text:</strong> "{visionResult.raw_ocr_text}"
                        </div>
                      )}

                      <div style={{ marginTop: '16px', paddingTop: '16px', borderTop: '1px solid #BBF7D0' }}>
                        <div style={{ fontSize: '14px', fontWeight: 700, color: '#166534', marginBottom: '8px' }}>
                          AI Step-by-Step Solution Breakdown:
                        </div>
                        <div style={{ fontSize: '14px', lineHeight: 1.6, color: '#1F2937' }}>
                          {renderFormattedTutorText(
                            visionResult.ai_solution || visionResult.explanation || `### Solution for: ${visionResult.question || 'Question'}\n\nNo detailed solution generated.`
                          )}
                        </div>
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          </ErrorBoundary>
        );

      case 'voice':
        return (
          <div className="card-box" style={{ textAlign: 'center', padding: '40px 20px' }}>
            <h2 className="section-title" style={{ justifyContent: 'center' }}>🎤 Voice AI Assistant</h2>
            <p style={{ color: '#64748B', fontSize: '14px', marginBottom: '24px' }}>
              Speak your doubt naturally. LearnSync AI transcribes and answers in real-time.
            </p>

            {/* Pulsing Mic Circle */}
            <div
              style={{
                width: '100px',
                height: '100px',
                borderRadius: '50%',
                backgroundColor: isListeningVoice ? '#EF4444' : '#EEF2FF',
                color: isListeningVoice ? '#FFFFFF' : '#4F46E5',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '40px',
                margin: '0 auto 20px auto',
                boxShadow: isListeningVoice ? '0 0 0 16px rgba(239, 68, 68, 0.2)' : '0 0 0 12px rgba(79, 70, 229, 0.1)',
                cursor: 'pointer',
                transition: 'all 0.2s ease'
              }}
              onClick={isListeningVoice ? handleStopListening : handleStartListening}
            >
              {isListeningVoice ? <StopIcon size={36} /> : <MicIcon size={36} />}
            </div>

            <div style={{ fontSize: '15px', fontWeight: 700, color: '#0F172A', marginBottom: '16px' }}>
              {isListeningVoice ? '🔴 Listening… speak now' : voiceState === 'processing' ? '⏳ Processing transcript…' : 'Tap microphone to start speaking'}
            </div>

            <div style={{ display: 'flex', justifyContent: 'center', gap: '10px', marginBottom: '24px' }}>
              {!isListeningVoice ? (
                <Button
                  variant="primary"
                  size="md"
                  icon={<MicIcon size={16} />}
                  onClick={handleStartListening}
                >
                  Start Voice Assistant
                </Button>
              ) : (
                <Button
                  variant="danger"
                  size="md"
                  icon={<StopIcon size={16} />}
                  onClick={handleStopListening}
                >
                  Stop & Process Query
                </Button>
              )}
            </div>

            {/* Live Transcript / Question Display */}
            {voiceTranscript && (
              <div style={{ maxWidth: '600px', margin: '0 auto 20px auto', textAlign: 'left', padding: '16px', backgroundColor: '#F8FAFC', borderRadius: '12px', border: '1px solid #E2E8F0' }}>
                <div style={{ fontSize: '12px', fontWeight: 700, color: '#64748B', textTransform: 'uppercase', marginBottom: '4px' }}>
                  Captured Speech Transcript:
                </div>
                <div style={{ fontSize: '15px', color: '#0F172A', fontWeight: 600 }}>
                  "{voiceTranscript}"
                </div>
              </div>
            )}

            {/* Voice AI Response */}
            {voiceAiResponse && (
              <div style={{ maxWidth: '700px', margin: '0 auto', textAlign: 'left', padding: '20px', backgroundColor: '#FFFFFF', borderRadius: '16px', border: '1px solid #C7D2FE', boxShadow: '0 4px 12px rgba(79,70,229,0.08)' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                  <span style={{ fontSize: '15px', fontWeight: 700, color: '#3730A3', display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <SparklesIcon size={18} /> Voice AI Response
                  </span>
                  <Button
                    variant="outline"
                    size="sm"
                    icon={isPlayingAudio ? <StopIcon size={14} /> : <PlayIcon size={14} />}
                    onClick={() => handleReadAloud(voiceAiResponse)}
                  >
                    {isPlayingAudio ? 'Stop Audio' : 'Listen Aloud 🔊'}
                  </Button>
                </div>

                <div style={{ marginBottom: '16px' }}>
                  {renderFormattedTutorText(voiceAiResponse)}
                </div>

                {voiceFollowups.length > 0 && (
                  <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap', paddingTop: '12px', borderTop: '1px solid #EEF2FF' }}>
                    {voiceFollowups.map((chip, idx) => (
                      <button
                        key={idx}
                        onClick={() => {
                          setTutorQuery(chip);
                          setActiveTab('tutor');
                        }}
                        style={{
                          padding: '6px 12px',
                          borderRadius: '16px',
                          backgroundColor: '#EEF2FF',
                          border: '1px solid #C7D2FE',
                          color: '#3730A3',
                          fontSize: '12px',
                          fontWeight: 600,
                          cursor: 'pointer'
                        }}
                      >
                        💡 {chip}
                      </button>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>
        );

      case 'assessments':
        return (
          <div className="card-box">
            <h2 className="section-title">📝 Adaptive Assessments</h2>
            <p style={{ color: '#64748B', fontSize: '14px', marginBottom: '20px' }}>
              Dynamic difficulty quizzes adjusting to your individual mastery level.
            </p>

            {!activeAssessment ? (
              <div style={{ padding: '24px', backgroundColor: '#F8FAFC', borderRadius: '16px', border: '1px solid #E2E8F0' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px', flexWrap: 'wrap', gap: '8px' }}>
                  <span style={{ fontWeight: 700, fontSize: '16px', color: '#0F172A' }}>
                    Computer Networks — Transport Layer Adaptive Challenge
                  </span>
                  <span style={{ backgroundColor: '#DCFCE7', color: '#166534', padding: '4px 12px', borderRadius: '12px', fontSize: '12px', fontWeight: 700 }}>
                    Adaptive Ready
                  </span>
                </div>
                <p style={{ fontSize: '14px', color: '#64748B', marginBottom: '20px' }}>
                  5 Questions • Real-Time Difficulty Scaling • Instant AI Evaluation & Feedback
                </p>
                <Button
                  variant="primary"
                  size="lg"
                  loading={assessmentLoading}
                  icon={<SparklesIcon size={18} />}
                  onClick={handleStartAssessment}
                >
                  {assessmentLoading ? 'Preparing your adaptive assessment…' : 'Start Assessment'}
                </Button>
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                {/* Assessment Header */}
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '16px 20px', backgroundColor: '#EEF2FF', borderRadius: '14px', border: '1px solid #C7D2FE' }}>
                  <div>
                    <div style={{ fontSize: '16px', fontWeight: 800, color: '#3730A3' }}>
                      {activeAssessment.subject} — {activeAssessment.topic}
                    </div>
                    <div style={{ fontSize: '13px', color: '#4338CA', marginTop: '2px' }}>
                      Question {currentQuestionIndex + 1} of {activeAssessment.questions.length}
                    </div>
                  </div>
                  <span style={{ backgroundColor: '#FFFFFF', color: '#4F46E5', fontWeight: 700, padding: '4px 12px', borderRadius: '12px', fontSize: '12px' }}>
                    Mode: {activeAssessment.requested_difficulty}
                  </span>
                </div>

                {/* Question Item Card */}
                {!assessmentSubmitted ? (
                  (() => {
                    const q = activeAssessment.questions[currentQuestionIndex];
                    const selected = selectedAnswers[q.id];

                    return (
                      <div style={{ padding: '24px', backgroundColor: '#FFFFFF', borderRadius: '16px', border: '1px solid #E2E8F0' }}>
                        <div style={{ fontSize: '13px', fontWeight: 700, color: '#4F46E5', textTransform: 'uppercase', marginBottom: '8px' }}>
                          Question {currentQuestionIndex + 1} • {q.topic}
                        </div>
                        <h3 style={{ fontSize: '17px', fontWeight: 700, color: '#0F172A', marginBottom: '20px', lineHeight: 1.4 }}>
                          {q.question}
                        </h3>

                        <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginBottom: '24px' }}>
                          {q.options.map((opt) => {
                            const isSelected = selected === opt.key;
                            return (
                              <div
                                key={opt.key}
                                onClick={() => handleSelectOption(q.id, opt.key)}
                                style={{
                                  padding: '14px 18px',
                                  borderRadius: '12px',
                                  border: isSelected ? '2px solid #4F46E5' : '1px solid #CBD5E1',
                                  backgroundColor: isSelected ? '#EEF2FF' : '#FFFFFF',
                                  color: isSelected ? '#3730A3' : '#0F172A',
                                  fontWeight: isSelected ? 700 : 500,
                                  cursor: 'pointer',
                                  display: 'flex',
                                  alignItems: 'center',
                                  gap: '12px',
                                  transition: 'all 0.15s ease'
                                }}
                              >
                                <span style={{
                                  width: '24px',
                                  height: '24px',
                                  borderRadius: '50%',
                                  backgroundColor: isSelected ? '#4F46E5' : '#F1F5F9',
                                  color: isSelected ? '#FFFFFF' : '#475569',
                                  display: 'flex',
                                  alignItems: 'center',
                                  justifyContent: 'center',
                                  fontSize: '12px',
                                  fontWeight: 700
                                }}>
                                  {opt.key}
                                </span>
                                <span>{opt.text}</span>
                              </div>
                            );
                          })}
                        </div>

                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <Button
                            variant="secondary"
                            size="md"
                            disabled={currentQuestionIndex === 0}
                            onClick={() => setCurrentQuestionIndex(prev => prev - 1)}
                          >
                            Previous
                          </Button>

                          {currentQuestionIndex < activeAssessment.questions.length - 1 ? (
                            <Button
                              variant="primary"
                              size="md"
                              onClick={() => setCurrentQuestionIndex(prev => prev + 1)}
                            >
                              Next Question
                            </Button>
                          ) : (
                            <Button
                              variant="success"
                              size="md"
                              loading={evaluatingAssessment}
                              onClick={handleSubmitAssessment}
                            >
                              Submit Assessment
                            </Button>
                          )}
                        </div>
                      </div>
                    );
                  })()
                ) : (
                  /* Assessment Evaluation Summary */
                  assessmentResult && (
                    <div style={{ padding: '24px', backgroundColor: '#F0FDF4', borderRadius: '16px', border: '1px solid #86EFAC' }}>
                      <div style={{ textAlign: 'center', marginBottom: '24px' }}>
                        <div style={{ fontSize: '48px', fontWeight: 800, color: '#166534' }}>
                          {assessmentResult.score} / {assessmentResult.total}
                        </div>
                        <div style={{ fontSize: '18px', fontWeight: 700, color: '#15803D' }}>
                          Overall Mastery Score: {assessmentResult.percentage}%
                        </div>
                      </div>

                      <div style={{ backgroundColor: '#FFFFFF', padding: '16px', borderRadius: '12px', border: '1px solid #CBD5E1', marginBottom: '16px' }}>
                        <div style={{ fontSize: '14px', fontWeight: 700, color: '#0F172A', marginBottom: '6px' }}>
                          🤖 AI Mastery Recommendation:
                        </div>
                        <p style={{ fontSize: '14px', color: '#334155', margin: 0, lineHeight: 1.5 }}>
                          {assessmentResult.ai_recommendation}
                        </p>
                      </div>

                      <div style={{ display: 'flex', gap: '12px', marginTop: '20px' }}>
                        <Button
                          variant="primary"
                          size="md"
                          onClick={handleStartAssessment}
                        >
                          Try Another Challenge
                        </Button>
                        <Button
                          variant="secondary"
                          size="md"
                          onClick={() => setActiveAssessment(null)}
                        >
                          Back to Assessments
                        </Button>
                      </div>
                    </div>
                  )
                )}
              </div>
            )}
          </div>
        );

      case 'progress':
        return (
          <div className="card-box">
            <h2 className="section-title">📊 Learning Profile & Skill Matrix</h2>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '14px', marginBottom: '6px' }}>
                  <span>Computer Networks (Overall Mastery)</span>
                  <strong>78%</strong>
                </div>
                <div style={{ height: '8px', backgroundColor: '#E2E8F0', borderRadius: '4px', overflow: 'hidden' }}>
                  <div style={{ width: '78%', height: '100%', backgroundColor: '#4F46E5' }}></div>
                </div>
              </div>
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '14px', marginBottom: '6px' }}>
                  <span>Operating Systems (Process Scheduling)</span>
                  <strong>65%</strong>
                </div>
                <div style={{ height: '8px', backgroundColor: '#E2E8F0', borderRadius: '4px', overflow: 'hidden' }}>
                  <div style={{ width: '65%', height: '100%', backgroundColor: '#0EA5E9' }}></div>
                </div>
              </div>
            </div>
          </div>
        );

      case 'profile':
        return (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <div className="card-box">
              <h2 className="section-title">👤 Student Account & Settings</h2>
              <div style={{ display: 'flex', gap: '16px', alignItems: 'center', marginBottom: '24px' }}>
                <div style={{ width: '60px', height: '60px', borderRadius: '50%', backgroundColor: '#4F46E5', color: '#FFFFFF', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '24px', fontWeight: 800 }}>
                  {user?.name?.[0] || 'S'}
                </div>
                <div>
                  <div style={{ fontSize: '18px', fontWeight: 700 }}>{user?.name || 'Santhosh'}</div>
                  <div style={{ fontSize: '14px', color: '#64748B' }}>{user?.email || 'student@learnsync.ai'}</div>
                  <div style={{ fontSize: '12px', color: '#4F46E5', fontWeight: 600, marginTop: '2px' }}>Role: STUDENT</div>
                </div>
              </div>

              <div style={{ borderTop: '1px solid #E2E8F0', paddingTop: '18px' }}>
                <div style={{ fontSize: '12px', fontWeight: 700, color: '#64748B', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '10px' }}>
                  Account Actions
                </div>
                <Button
                  variant="danger"
                  size="md"
                  icon={<LogoutIcon size={16} />}
                  onClick={() => { authService.logout(); onLogout(); }}
                >
                  Sign Out
                </Button>
              </div>
            </div>

            <div className="card-box">
              <div style={{ fontSize: '12px', fontWeight: 700, color: '#64748B', textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '14px' }}>
                About LearnSync AI
              </div>
              <div style={{ display: 'flex', gap: '16px', alignItems: 'flex-start' }}>
                <img
                  src="/assets/learnsync-ai-logo.png"
                  alt="LearnSync AI"
                  style={{ width: '52px', height: '52px', borderRadius: '12px', objectFit: 'contain', flexShrink: 0 }}
                />
                <div style={{ flex: 1 }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
                    <div style={{ fontSize: '18px', fontWeight: 800, color: '#0F172A' }}>LearnSync AI</div>
                    <span style={{
                      fontSize: '11px',
                      fontWeight: 700,
                      padding: '3px 9px',
                      borderRadius: '12px',
                      backgroundColor: '#EEF2FF',
                      color: '#3730A3',
                      border: '1px solid #C7D2FE'
                    }}>
                      v1.0 • Operational
                    </span>
                  </div>
                  <div style={{ fontSize: '13.5px', fontWeight: 600, color: '#4F46E5', marginBottom: '6px' }}>
                    Connecting Every Learner to Smarter Learning
                  </div>
                  <div style={{ fontSize: '13px', color: '#64748B', lineHeight: 1.4 }}>
                    AI-powered personalized learning platform for students and educators.
                  </div>
                </div>
              </div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="app-layout">
      {/* Student Sidebar Navigation */}
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">
            <img src="/assets/learnsync-ai-logo.png" alt="LearnSync AI" style={{ width: '100%', height: '100%', borderRadius: '10px', objectFit: 'contain' }} />
          </div>
          <div>
            <div className="brand-title">LearnSync AI</div>
            <div className="brand-subtitle">Student Web App</div>
          </div>
        </div>

        <ul className="nav-menu">
          {[
            { id: 'home', label: 'Home', icon: '🏠' },
            { id: 'tutor', label: 'AI Tutor', icon: '🤖' },
            { id: 'vision', label: 'Vision AI', icon: '📷' },
            { id: 'voice', label: 'Voice AI', icon: '🎤' },
            { id: 'assessments', label: 'Assessments', icon: '📝' },
            { id: 'progress', label: 'Progress', icon: '📊' },
            { id: 'profile', label: 'Profile', icon: '👤' },
          ].map((item) => (
            <li key={item.id}>
              <a
                href={`#/student/${item.id}`}
                className={`nav-item ${activeTab === item.id ? 'active' : ''}`}
                onClick={(e) => {
                  e.preventDefault();
                  setActiveTab(item.id);
                  window.location.hash = `/student/${item.id}`;
                }}
              >
                <span className="nav-icon">{item.icon}</span>
                <span>{item.label}</span>
              </a>
            </li>
          ))}
        </ul>

        {/* Student Logout Button */}
        <div style={{ marginTop: 'auto', paddingTop: '16px', borderTop: '1px solid #E2E8F0' }}>
          <Button
            variant="danger"
            size="sm"
            fullWidth
            icon={<LogoutIcon size={15} />}
            onClick={() => { authService.logout(); onLogout(); }}
          >
            Sign Out
          </Button>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="main-content">
        {renderTabContent()}
      </main>
    </div>
  );
}
