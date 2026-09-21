import React from 'react';
import { SpinnerIcon } from './Icons';

export default function Button({
  variant = 'primary',
  size = 'md',
  icon = null,
  children,
  onClick,
  type = 'button',
  disabled = false,
  loading = false,
  fullWidth = false,
  className = '',
  style = {},
  title = undefined,
  'aria-label': ariaLabel,
  ...props
}) {
  const baseClass = 'btn';
  const variantClass = `btn-${variant}`;
  const sizeClass = `btn-${size}`;
  const fullWidthClass = fullWidth ? 'btn-full-width' : '';
  const loadingClass = loading ? 'btn-loading' : '';

  const combinedClasses = [
    baseClass,
    variantClass,
    sizeClass,
    fullWidthClass,
    loadingClass,
    className
  ].filter(Boolean).join(' ');

  return (
    <button
      type={type}
      className={combinedClasses}
      onClick={onClick}
      disabled={disabled || loading}
      style={style}
      title={title}
      aria-label={ariaLabel || (typeof children === 'string' ? children : undefined)}
      {...props}
    >
      {loading ? (
        <span className="btn-icon">
          <SpinnerIcon size={size === 'sm' ? 14 : size === 'lg' ? 18 : 16} />
        </span>
      ) : icon ? (
        <span className="btn-icon">{icon}</span>
      ) : null}
      {children && <span className="btn-text">{children}</span>}
    </button>
  );
}
