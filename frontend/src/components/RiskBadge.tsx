import React from 'react';
import { ShieldAlert, ShieldCheck, AlertTriangle } from 'lucide-react';

interface RiskBadgeProps {
  level: 'LOW' | 'MEDIUM' | 'HIGH';
  size?: 'sm' | 'md' | 'lg';
}

export const RiskBadge: React.FC<RiskBadgeProps> = ({ level, size = 'md' }) => {
  const sizeClasses = {
    sm: 'text-xs px-2.5 py-0.5 gap-1 font-medium',
    md: 'text-xs px-3 py-1 gap-1.5 font-semibold',
    lg: 'text-sm px-4 py-1.5 gap-2 font-bold',
  };

  if (level === 'HIGH') {
    return (
      <span className={`inline-flex items-center rounded-md bg-destructive/15 text-destructive border border-destructive/30 ${sizeClasses[size]}`}>
        <ShieldAlert className="w-3.5 h-3.5 text-destructive" />
        HIGH RISK
      </span>
    );
  }

  if (level === 'MEDIUM') {
    return (
      <span className={`inline-flex items-center rounded-md bg-primary/15 text-primary border border-primary/30 ${sizeClasses[size]}`}>
        <AlertTriangle className="w-3.5 h-3.5 text-primary" />
        MEDIUM RISK
      </span>
    );
  }

  return (
    <span className={`inline-flex items-center rounded-md bg-success/15 text-success border border-success/30 ${sizeClasses[size]}`}>
      <ShieldCheck className="w-3.5 h-3.5 text-success" />
      LOW RISK
    </span>
  );
};
