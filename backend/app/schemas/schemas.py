from datetime import datetime
from typing import Optional, List, Any, Dict
from pydantic import BaseModel, EmailStr, Field

# User Schemas
class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: str
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# Scanning Request Schemas
class MessageScanRequest(BaseModel):
    text: str = Field(..., min_length=2, description="The suspicious SMS or message text")

class UrlScanRequest(BaseModel):
    url: str = Field(..., min_length=3, description="The URL to analyze")

class PhoneScanRequest(BaseModel):
    phone: str = Field(..., min_length=5, description="The phone number or customer care string")

class PaymentScanRequest(BaseModel):
    recipient: str = Field(..., description="Recipient name or handle")
    amount: Optional[float] = Field(None, description="Requested amount")
    message: Optional[str] = Field(None, description="Note or reason provided")
    upi_id: Optional[str] = Field(None, description="UPI ID if provided")
    phone: Optional[str] = Field(None, description="Contact phone")
    payment_method: Optional[str] = Field("UPI", description="UPI, NetBanking, Card, QR")

class FusionScanRequest(BaseModel):
    message: Optional[str] = None
    url: Optional[str] = None
    phone: Optional[str] = None
    upi_id: Optional[str] = None
    amount: Optional[float] = None
    recipient: Optional[str] = None

# Scan Result Schemas
class IndicatorDetail(BaseModel):
    category: str
    severity: str # LOW, MEDIUM, HIGH
    title: str
    description: str

class ScanResult(BaseModel):
    scan_id: Optional[str] = None
    scan_type: str
    risk_score: int = Field(..., ge=0, le=100)
    risk_level: str # LOW, MEDIUM, HIGH
    confidence: str # low, medium, high
    indicators: List[IndicatorDetail]
    explanation: str
    recommendation: str
    created_at: Optional[datetime] = None
    extracted_metadata: Optional[Dict[str, Any]] = None

class ScanResponse(BaseModel):
    id: str
    scan_type: str
    risk_score: int
    risk_level: str
    confidence: str
    indicators: List[Any]
    explanation: str
    recommendation: str
    created_at: datetime
    class Config:
        from_attributes = True

# Report Schemas
class ReportCreate(BaseModel):
    scam_type: str
    description: str
    evidence_url: Optional[str] = None
    evidence_phone: Optional[str] = None
    scan_id: Optional[str] = None

class ReportResponse(BaseModel):
    id: str
    scam_type: str
    description: str
    created_at: datetime
    class Config:
        from_attributes = True

# Admin / Statistics Schemas
class StatisticsResponse(BaseModel):
    total_scans: int
    high_risk_count: int
    medium_risk_count: int
    low_risk_count: int
    scans_by_type: Dict[str, int]
    top_indicators: List[Dict[str, Any]]
    recent_scans: List[ScanResponse]
