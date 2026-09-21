import React, { useEffect } from 'react';
import Button from './Button';
import { XIcon, AlertCircleIcon } from './Icons';

export default function ConfirmModal({
  isOpen,
  title = 'Confirm Action',
  message = 'Are you sure you want to proceed?',
  confirmText = 'Confirm',
  cancelText = 'Cancel',
  confirmVariant = 'danger',
  isLoading = false,
  onConfirm,
  onCancel
}) {
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape' && isOpen && !isLoading) {
        onCancel();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, isLoading, onCancel]);

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={() => !isLoading && onCancel()} role="dialog" aria-modal="true" aria-labelledby="confirm-modal-title">
      <div className="modal-content" style={{ maxWidth: '440px' }} onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <span style={{ color: confirmVariant === 'danger' ? '#EF4444' : '#4F46E5', display: 'flex' }}>
              <AlertCircleIcon size={22} />
            </span>
            <h3 id="confirm-modal-title" className="modal-title" style={{ fontSize: '17px' }}>
              {title}
            </h3>
          </div>
          <button
            onClick={() => !isLoading && onCancel()}
            aria-label="Close dialog"
            style={{
              background: 'none',
              border: 'none',
              cursor: 'pointer',
              color: '#94A3B8',
              padding: '4px',
              borderRadius: '6px'
            }}
          >
            <XIcon size={16} />
          </button>
        </div>

        <div style={{ margin: '16px 0 24px 0', color: '#475569', fontSize: '14px', lineHeight: '1.5' }}>
          {message}
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '10px' }}>
          <Button variant="secondary" size="md" onClick={onCancel} disabled={isLoading}>
            {cancelText}
          </Button>
          <Button variant={confirmVariant} size="md" onClick={onConfirm} loading={isLoading}>
            {confirmText}
          </Button>
        </div>
      </div>
    </div>
  );
}
