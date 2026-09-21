import { ScanResult, StatisticsResponse, ScanRecord } from '../types';

const API_BASE_URL = 'http://127.0.0.1:8000/api';

export const apiService = {
  // Scans
  scanMessage: async (text: string): Promise<ScanResult> => {
    const res = await fetch(`${API_BASE_URL}/scan/message`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text }),
    });
    if (!res.ok) throw new Error((await res.json()).detail || 'Failed to scan message');
    return res.json();
  },

  scanUrl: async (url: string): Promise<ScanResult> => {
    const res = await fetch(`${API_BASE_URL}/scan/url`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url }),
    });
    if (!res.ok) throw new Error((await res.json()).detail || 'Failed to scan URL');
    return res.json();
  },

  scanQr: async (file: File): Promise<ScanResult> => {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`${API_BASE_URL}/scan/qr`, {
      method: 'POST',
      body: formData,
    });
    if (!res.ok) throw new Error((await res.json()).detail || 'Failed to scan QR code');
    return res.json();
  },

  scanPhone: async (phone: string): Promise<ScanResult> => {
    const res = await fetch(`${API_BASE_URL}/scan/phone`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ phone }),
    });
    if (!res.ok) throw new Error((await res.json()).detail || 'Failed to scan phone number');
    return res.json();
  },

  scanPayment: async (data: {
    recipient: string;
    amount?: number;
    message?: string;
    upi_id?: string;
    phone?: string;
    payment_method?: string;
  }): Promise<ScanResult> => {
    const res = await fetch(`${API_BASE_URL}/scan/payment`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error((await res.json()).detail || 'Failed to scan payment request');
    return res.json();
  },

  scanScreenshot: async (file: File): Promise<ScanResult> => {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`${API_BASE_URL}/scan/screenshot`, {
      method: 'POST',
      body: formData,
    });
    if (!res.ok) throw new Error((await res.json()).detail || 'Failed to scan screenshot');
    return res.json();
  },

  scanFusion: async (data: {
    message?: string;
    url?: string;
    phone?: string;
    upi_id?: string;
    amount?: number;
    recipient?: string;
  }): Promise<ScanResult> => {
    const res = await fetch(`${API_BASE_URL}/scan/fusion`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error((await res.json()).detail || 'Failed to execute fusion scan');
    return res.json();
  },

  // History
  getScans: async (filter?: { risk_level?: string; scan_type?: string }): Promise<ScanRecord[]> => {
    const params = new URLSearchParams();
    if (filter?.risk_level && filter.risk_level !== 'ALL') params.append('risk_level', filter.risk_level);
    if (filter?.scan_type && filter.scan_type !== 'ALL') params.append('scan_type', filter.scan_type);
    const res = await fetch(`${API_BASE_URL}/scans?${params.toString()}`);
    if (!res.ok) throw new Error('Failed to fetch scans');
    return res.json();
  },

  deleteScan: async (id: string): Promise<void> => {
    const res = await fetch(`${API_BASE_URL}/scans/${id}`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Failed to delete scan');
  },

  // Reports
  submitReport: async (data: {
    scam_type: string;
    description: string;
    evidence_url?: string;
    evidence_phone?: string;
    scan_id?: string;
  }): Promise<any> => {
    const res = await fetch(`${API_BASE_URL}/reports`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error('Failed to submit report');
    return res.json();
  },

  // Statistics
  getStatistics: async (): Promise<StatisticsResponse> => {
    const res = await fetch(`${API_BASE_URL}/admin/statistics`);
    if (!res.ok) throw new Error('Failed to fetch statistics');
    return res.json();
  }
};
