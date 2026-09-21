import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    scans = relationship("Scan", back_populates="user", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="user", cascade="all, delete-orphan")


class Scan(Base):
    __tablename__ = "scans"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True) # allow anonymous scans for demo
    scan_type = Column(String(50), nullable=False)  # message, url, qr, phone, payment, screenshot
    input_hash = Column(String(64), nullable=True)  # SHA-256 of input for privacy-preserving deduplication
    risk_score = Column(Integer, nullable=False)    # 0 to 100
    risk_level = Column(String(20), nullable=False) # LOW, MEDIUM, HIGH
    confidence = Column(String(20), nullable=False) # low, medium, high
    indicators = Column(JSON, nullable=False)       # list of detected indicator dicts/strings
    explanation = Column(Text, nullable=False)
    recommendation = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="scans")
    details = relationship("ScanDetail", back_populates="scan", uselist=False, cascade="all, delete-orphan")


class ScanDetail(Base):
    __tablename__ = "scan_details"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    scan_id = Column(String(36), ForeignKey("scans.id"), unique=True, nullable=False)
    message_features = Column(JSON, nullable=True)
    url_features = Column(JSON, nullable=True)
    qr_features = Column(JSON, nullable=True)
    phone_features = Column(JSON, nullable=True)
    payment_features = Column(JSON, nullable=True)
    raw_summary = Column(Text, nullable=True)

    scan = relationship("Scan", back_populates="details")


class Report(Base):
    __tablename__ = "reports"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    scan_id = Column(String(36), ForeignKey("scans.id"), nullable=True)
    scam_type = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    evidence_url = Column(String(500), nullable=True)
    evidence_phone = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="reports")
