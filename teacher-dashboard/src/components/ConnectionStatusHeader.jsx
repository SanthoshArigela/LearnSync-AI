import React, { useState } from 'react';
import Button from './Button';
import ConfirmModal from './ConfirmModal';
import { useToast } from './Toast';
import { RefreshIcon, PlusIcon } from './Icons';

import { getApiUrl } from '../config/apiConfig';

export default function ConnectionStatusHeader({ isConnected, isRestFallback, lastSync, onTriggerDemoEvent }) {
  const toast = useToast();
  const [demoActive, setDemoActive] = useState(false);
  const [showResetModal, setShowResetModal] = useState(false);
  const [isResetting, setIsResetting] = useState(false);

  const handleSimulate = () => {
    setDemoActive(true);
    toast.info('Simulating active student learning event...');
    if (onTriggerDemoEvent) {
      onTriggerDemoEvent();
    }
    setTimeout(() => {
      setDemoActive(false);
      toast.success('Student event simulated successfully.');
    }, 1200);
  };

  const handleConfirmReset = async () => {
    setIsResetting(true);
    try {
      await fetch(getApiUrl('/api/teacher/demo/reset'), { method: 'POST' });
      toast.success('Classroom demo state reset to baseline.');
      setTimeout(() => window.location.reload(), 800);
    } catch (err) {
      toast.error('Failed to reset demo state. Refreshing page...');
      setTimeout(() => window.location.reload(), 1000);
    } finally {
      setIsResetting(false);
      setShowResetModal(false);
    }
  };

  return (
    <>
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          backgroundColor: '#FFFFFF',
          border: '1px solid #E2E8F0',
          borderRadius: '16px',
          padding: '12px 20px',
          marginBottom: '24px'
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px', flexWrap: 'wrap' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span
              style={{
                width: '10px',
                height: '10px',
                borderRadius: '50%',
                backgroundColor: isConnected ? '#10B981' : isRestFallback ? '#3B82F6' : '#EF4444',
                display: 'inline-block'
              }}
            ></span>
            <span style={{ fontSize: '13.5px', fontWeight: 700, color: '#0F172A' }}>
              {isConnected ? 'Live WebSocket Connected' : isRestFallback ? 'REST Sync Active' : 'Offline Mode'}
            </span>
          </div>

          <span style={{ fontSize: '13px', color: '#64748B' }}>
            Class: <strong>B.Tech CSE — AI & ML (Sec A)</strong>
          </span>

          <span style={{ fontSize: '12.5px', color: '#94A3B8' }}>
            • Last sync: {lastSync || 'Just now'}
          </span>
        </div>

        <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
          <Button
            variant="danger"
            size="sm"
            icon={<RefreshIcon size={14} />}
            onClick={() => setShowResetModal(true)}
          >
            Reset Demo
          </Button>

          <Button
            variant="secondary"
            size="sm"
            icon={<PlusIcon size={14} />}
            onClick={handleSimulate}
            loading={demoActive}
          >
            {demoActive ? 'Simulating...' : 'Simulate Student Event'}
          </Button>
        </div>
      </div>

      <ConfirmModal
        isOpen={showResetModal}
        title="Reset Demo State"
        message="Are you sure you want to reset classroom demo analytics to baseline dataset? All live event triggers will be cleared."
        confirmText="Reset Demo"
        confirmVariant="danger"
        isLoading={isResetting}
        onConfirm={handleConfirmReset}
        onCancel={() => setShowResetModal(false)}
      />
    </>
  );
}
