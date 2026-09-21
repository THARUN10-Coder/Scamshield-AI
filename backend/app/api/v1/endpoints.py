import hashlib
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.core.database import get_db
from app.core.config import settings
from app.models.models import User, Scan, ScanDetail, Report
from app.schemas.schemas import (
    UserCreate, UserLogin, UserResponse, Token,
    MessageScanRequest, UrlScanRequest, PhoneScanRequest,
    PaymentScanRequest, FusionScanRequest, ScanResult, ScanResponse,
    ReportCreate, ReportResponse, StatisticsResponse
)
from app.security.auth import verify_password, get_password_hash, create_access_token
from app.services.message_service import MLScamService
from app.services.url_service import URLScannerService
from app.services.qr_service import QRScannerService
from app.services.phone_service import PhoneScannerService
from app.services.payment_service import PaymentRequestService
from app.services.screenshot_service import ScreenshotScannerService
from app.services.fusion_service import MultiSignalFusionEngine

api_router = APIRouter()

# Instantiate Singletons
message_service = MLScamService()
url_service = URLScannerService()
qr_service = QRScannerService()
phone_service = PhoneScannerService()
payment_service = PaymentRequestService()
screenshot_service = ScreenshotScannerService()
fusion_service = MultiSignalFusionEngine()

# Helpers
def get_current_user_optional(db: Session = Depends(get_db)) -> Optional[User]:
    # Allows both authenticated users and anonymous demonstration scans
    return None

def record_scan_audit(
    db: Session,
    scan_type: str,
    raw_input: str,
    result: dict,
    user_id: Optional[str] = None
) -> Scan:
    input_hash = hashlib.sha256(raw_input.encode("utf-8")).hexdigest() if raw_input else None
    scan = Scan(
        user_id=user_id,
        scan_type=scan_type,
        input_hash=input_hash,
        risk_score=result["risk_score"],
        risk_level=result["risk_level"],
        confidence=result["confidence"],
        indicators=result["indicators"],
        explanation=result["explanation"],
        recommendation=result["recommendation"]
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)

    # Save detailed features
    detail = ScanDetail(
        scan_id=scan.id,
        message_features=result.get("extracted_metadata", {}).get("message_features"),
        url_features=result.get("extracted_metadata", {}).get("url_analysis"),
        qr_features=result.get("extracted_metadata") if scan_type == "qr" else None,
        phone_features=result.get("extracted_metadata") if scan_type == "phone" else None,
        payment_features=result.get("extracted_metadata") if scan_type in ["payment", "fusion"] else None,
        raw_summary=raw_input[:120] if raw_input else ""
    )
    db.add(detail)
    db.commit()

    return scan


# ==========================================
# AUTHENTICATION ENDPOINTS
# ==========================================

@api_router.post("/auth/register", response_model=Token)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_in.email.lower()).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address is already registered."
        )
    user = User(
        name=user_in.name,
        email=user_in.email.lower(),
        password_hash=get_password_hash(user_in.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    token = create_access_token(data={"sub": user.email, "id": user.id})
    return {"access_token": token, "token_type": "bearer", "user": user}

@api_router.post("/auth/login", response_model=Token)
def login(login_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_in.email.lower()).first()
    if not user or not verify_password(login_in.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password credentials."
        )
    token = create_access_token(data={"sub": user.email, "id": user.id})
    return {"access_token": token, "token_type": "bearer", "user": user}

@api_router.get("/auth/me", response_model=UserResponse)
def get_me(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid session token.")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user


# ==========================================
# SCANNING ENDPOINTS
# ==========================================

@api_router.post("/scan/message", response_model=ScanResult)
def scan_message(req: MessageScanRequest, db: Session = Depends(get_db)):
    result = message_service.predict_text(req.text)
    scan = record_scan_audit(db, "message", req.text, result)
    result["scan_id"] = scan.id
    result["scan_type"] = "message"
    result["created_at"] = scan.created_at
    return result

@api_router.post("/scan/url", response_model=ScanResult)
def scan_url(req: UrlScanRequest, db: Session = Depends(get_db)):
    result = url_service.scan_url(req.url)
    scan = record_scan_audit(db, "url", req.url, result)
    result["scan_id"] = scan.id
    result["scan_type"] = "url"
    result["created_at"] = scan.created_at
    return result

@api_router.post("/scan/qr", response_model=ScanResult)
async def scan_qr(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image file exceeds 10MB limit.")
    result = qr_service.decode_and_analyze(contents, file.filename or "")
    if not result.get("success", False):
        raise HTTPException(status_code=400, detail=result.get("error", "Unable to decode QR code."))

    raw_summary = result.get("extracted_metadata", {}).get("raw_payload", "QR_CODE")
    scan = record_scan_audit(db, "qr", raw_summary, result)
    result["scan_id"] = scan.id
    result["scan_type"] = "qr"
    result["created_at"] = scan.created_at
    return result

@api_router.post("/scan/phone", response_model=ScanResult)
def scan_phone(req: PhoneScanRequest, db: Session = Depends(get_db)):
    result = phone_service.scan_phone(req.phone)
    scan = record_scan_audit(db, "phone", req.phone, result)
    result["scan_id"] = scan.id
    result["scan_type"] = "phone"
    result["created_at"] = scan.created_at
    return result

@api_router.post("/scan/payment", response_model=ScanResult)
def scan_payment(req: PaymentScanRequest, db: Session = Depends(get_db)):
    result = payment_service.analyze_payment(
        recipient=req.recipient,
        amount=req.amount,
        message=req.message,
        upi_id=req.upi_id,
        phone=req.phone,
        payment_method=req.payment_method or "UPI"
    )
    raw_summary = f"{req.recipient} | ₹{req.amount or 0} | {req.upi_id or ''}"
    scan = record_scan_audit(db, "payment", raw_summary, result)
    result["scan_id"] = scan.id
    result["scan_type"] = "payment"
    result["created_at"] = scan.created_at
    return result

@api_router.post("/scan/screenshot", response_model=ScanResult)
async def scan_screenshot(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Screenshot exceeds 10MB limit.")
    result = screenshot_service.scan_image(contents, file.filename or "")
    if not result.get("success", False):
        raise HTTPException(status_code=400, detail=result.get("error", "Failed to analyze screenshot."))

    raw_summary = result.get("extracted_metadata", {}).get("extracted_text", "SCREENSHOT")
    scan = record_scan_audit(db, "screenshot", raw_summary, result)
    result["scan_id"] = scan.id
    result["scan_type"] = "screenshot"
    result["created_at"] = scan.created_at
    return result

@api_router.post("/scan/fusion", response_model=ScanResult)
def scan_fusion(req: FusionScanRequest, db: Session = Depends(get_db)):
    result = fusion_service.fuse_signals(
        message=req.message,
        url=req.url,
        phone=req.phone,
        upi_id=req.upi_id,
        amount=req.amount,
        recipient=req.recipient
    )
    raw_summary = f"Fusion: {req.recipient or ''} | {req.url or ''} | {req.phone or ''}"
    scan = record_scan_audit(db, "fusion", raw_summary, result)
    result["scan_id"] = scan.id
    result["scan_type"] = "fusion"
    result["created_at"] = scan.created_at
    return result


# ==========================================
# SCAN HISTORY ENDPOINTS
# ==========================================

@api_router.get("/scans", response_model=list[ScanResponse])
def get_scans(
    limit: int = 50,
    risk_level: Optional[str] = None,
    scan_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Scan)
    if risk_level:
        query = query.filter(Scan.risk_level == risk_level.upper())
    if scan_type:
        query = query.filter(Scan.scan_type == scan_type.lower())
    return query.order_by(Scan.created_at.desc()).limit(limit).all()

@api_router.get("/scans/{scan_id}", response_model=ScanResponse)
def get_scan(scan_id: str, db: Session = Depends(get_db)):
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan record not found.")
    return scan

@api_router.delete("/scans/{scan_id}")
def delete_scan(scan_id: str, db: Session = Depends(get_db)):
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan record not found.")
    db.delete(scan)
    db.commit()
    return {"message": "Scan record deleted successfully."}


# ==========================================
# REPORT SCAM ENDPOINTS
# ==========================================

@api_router.post("/reports", response_model=ReportResponse)
def create_report(req: ReportCreate, db: Session = Depends(get_db)):
    report = Report(
        scam_type=req.scam_type,
        description=req.description,
        evidence_url=req.evidence_url,
        evidence_phone=req.evidence_phone,
        scan_id=req.scan_id
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    return report


# ==========================================
# ADMIN & STATISTICS ENDPOINTS
# ==========================================

@api_router.get("/admin/statistics", response_model=StatisticsResponse)
def get_statistics(db: Session = Depends(get_db)):
    total_scans = db.query(Scan).count()
    high_risk_count = db.query(Scan).filter(Scan.risk_level == "HIGH").count()
    medium_risk_count = db.query(Scan).filter(Scan.risk_level == "MEDIUM").count()
    low_risk_count = db.query(Scan).filter(Scan.risk_level == "LOW").count()

    # Aggregate by type
    scans = db.query(Scan).all()
    scans_by_type = {}
    indicator_counts = {}

    for s in scans:
        scans_by_type[s.scan_type] = scans_by_type.get(s.scan_type, 0) + 1
        if isinstance(s.indicators, list):
            for ind in s.indicators:
                if isinstance(ind, dict) and "category" in ind:
                    cat = ind["category"]
                    indicator_counts[cat] = indicator_counts.get(cat, 0) + 1

    top_indicators = [
        {"indicator": k, "count": v}
        for k, v in sorted(indicator_counts.items(), key=lambda x: x[1], reverse=True)[:6]
    ]

    recent_scans = db.query(Scan).order_by(Scan.created_at.desc()).limit(10).all()

    return {
        "total_scans": total_scans,
        "high_risk_count": high_risk_count,
        "medium_risk_count": medium_risk_count,
        "low_risk_count": low_risk_count,
        "scans_by_type": scans_by_type,
        "top_indicators": top_indicators,
        "recent_scans": recent_scans
    }
