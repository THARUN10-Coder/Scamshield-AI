import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "ScamShield AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    SECRET_KEY: str = "scamshield-super-secret-jwt-key-change-in-production-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Database: SQLite by default for zero config, Postgres compatible
    DATABASE_URL: str = "sqlite:///./scamshield.db"
    
    # ML Models path
    ML_MODEL_PATH: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ml", "models")
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ]
    
    # Risk Thresholds
    LOW_RISK_THRESHOLD: int = 30
    HIGH_RISK_THRESHOLD: int = 70

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
