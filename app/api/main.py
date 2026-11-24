
import sys
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from src.detection.inference import analyze_security_event

app = FastAPI(
    title="CyberShield AI",
    description="AI-powered cybersecurity threat analysis",
    version="1.0"
)

class SecurityEvent(BaseModel):
    event: str
    duration: int
    protocol: str
    src_bytes: int
    dst_bytes: int
    failed_logins: int
    connection_count: int

@app.get("/")
def home():
    return {
        "project": "CyberShield AI",
        "status": "API is running"
    }

@app.post("/analyze")
def analyze_event(data: SecurityEvent):

    features = {
        "duration": data.duration,
        "protocol": data.protocol,
        "src_bytes": data.src_bytes,
        "dst_bytes": data.dst_bytes,
        "failed_logins": data.failed_logins,
        "connection_count": data.connection_count
    }

    result = analyze_security_event(data.event, features)

    return {
        "project": "CyberShield AI",
        "event": data.event,
        "analysis": result
    }
