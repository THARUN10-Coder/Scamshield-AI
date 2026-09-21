export interface IndicatorDetail {
  category: string;
  severity: 'LOW' | 'MEDIUM' | 'HIGH';
  title: string;
  description: string;
}

export interface ScanResult {
  scan_id?: string;
  scan_type: string;
  risk_score: number; // 0 - 100
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH';
  confidence: 'low' | 'medium' | 'high';
  indicators: IndicatorDetail[];
  explanation: string;
  recommendation: string;
  created_at?: string;
  extracted_metadata?: Record<string, any>;
}

export interface ScanRecord {
  id: string;
  scan_type: string;
  risk_score: number;
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH';
  confidence: string;
  indicators: IndicatorDetail[];
  explanation: string;
  recommendation: string;
  created_at: string;
}

export interface StatisticsResponse {
  total_scans: number;
  high_risk_count: number;
  medium_risk_count: number;
  low_risk_count: number;
  scans_by_type: Record<string, number>;
  top_indicators: { indicator: string; count: number }[];
  recent_scans: ScanRecord[];
}

export interface UserProfile {
  id: string;
  name: string;
  email: string;
}
