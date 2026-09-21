import React from 'react';
import Button from './Button';

export class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true, error };
  }

  componentDidCatch(error, errorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
  }

  handleRetry = () => {
    this.setState({ hasError: false, error: null });
    if (this.props.onReset) {
      this.props.onReset();
    }
  };

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: '30px', textAlign: 'center', backgroundColor: '#FEF2F2', borderRadius: '16px', border: '1px solid #FCA5A5', margin: '20px 0' }}>
          <div style={{ fontSize: '36px', marginBottom: '12px' }}>⚠️</div>
          <h3 style={{ fontSize: '18px', fontWeight: 700, color: '#991B1B', marginBottom: '8px' }}>
            {this.props.title || 'Vision AI encountered an unexpected error.'}
          </h3>
          <p style={{ fontSize: '14px', color: '#7F1D1D', marginBottom: '20px' }}>
            {this.props.message || 'Try selecting another image or refreshing the tab.'}
          </p>
          <Button variant="danger" size="md" onClick={this.handleRetry}>
            🔄 Retry Operation
          </Button>
        </div>
      );
    }
    return this.props.children;
  }
}

export default ErrorBoundary;
