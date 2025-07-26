from fastapi import FastAPI
from pydantic import BaseModel
import platform
import psutil
import subprocess
import os
import threading
import time
import requests
from datetime import timedelta

app = FastAPI()

# === Config ===
DJANGO_API_URL = "http://your-django-server/api/system-snapshot/"
SECURITY_ALERT_URL = "http://your-django-server/api/security-alerts/"
AUTH_TOKEN = "your-token-here"
DEVICE_ID = "your-managed-device-id"
AGENT_VERSION = "1.0.0"
# ==============

class SystemSnapshot(BaseModel):
    cpu_usage: float
    ram_used_mb: int
    disk_free_gb: float
    disk_used_percent: float
    net_recv_mb: float
    net_sent_mb: float
    uptime: str
    agent_version: str
    device_id: str

class SecurityAlert(BaseModel):
    device_id: str
    alert_type: str
    message: str
    extra_data: dict = {}

def get_uptime() -> str:
    if platform.system() == "Windows":
        try:
            output = subprocess.check_output("wmic os get lastbootuptime", shell=True).decode().splitlines()
            if len(output) > 1:
                return output[1].strip()
            return "Unknown"
        except Exception as e:
            return f"Error: {e}"
    else:
        try:
            with open("/proc/uptime", "r") as f:
                seconds = float(f.readline().split()[0])
                return str(timedelta(seconds=seconds))
        except Exception as e:
            return f"Error: {e}"

def collect_system_data():
    return {
        "cpu_usage": psutil.cpu_percent(),
        "ram_used_mb": psutil.virtual_memory().used // 1024**2,
        "disk_free_gb": psutil.disk_usage('/').free / 1024**3,
        "disk_used_percent": psutil.disk_usage('/').percent,
        "net_recv_mb": psutil.net_io_counters().bytes_recv / 1024**2,
        "net_sent_mb": psutil.net_io_counters().bytes_sent / 1024**2,
        "uptime": get_uptime(),
        "agent_version": AGENT_VERSION,
        "device_id": DEVICE_ID,
    }

def detect_failed_login_attempts(threshold=5):
    try:
        output = subprocess.check_output(
            "grep 'Failed password' /var/log/auth.log | tail -n 50", shell=True
        ).decode()
        attempts = output.strip().splitlines()
        return len(attempts) >= threshold
    except Exception as e:
        return False

def send_system_snapshot():
    while True:
        try:
            payload = collect_system_data()
            headers = {
                "Authorization": f"Token {AUTH_TOKEN}",
                "Content-Type": "application/json"
            }
            requests.post(DJANGO_API_URL, json=payload, headers=headers, timeout=5)
        except Exception as e:
            print(f"[Error] Failed to send system snapshot: {e}")
        time.sleep(60)

def send_security_alert(event_type, message, extra_data=None):
    try:
        payload = {
            "device_id": DEVICE_ID,
            "alert_type": event_type,
            "message": message,
            "extra_data": extra_data or {}
        }
        headers = {"Authorization": f"Token {AUTH_TOKEN}"}
        requests.post(SECURITY_ALERT_URL, json=payload, headers=headers, timeout=5)
    except Exception as e:
        print(f"Failed to send security alert: {e}")

def background_security_checks():
    while True:
        if detect_failed_login_attempts():
            send_security_alert(
                "brute_force",
                "More than 5 failed SSH login attempts detected.",
                {"count": 5}
            )
        time.sleep(30)

@app.on_event("startup")
def start_background_tasks():
    threading.Thread(target=send_system_snapshot, daemon=True).start()
    threading.Thread(target=background_security_checks, daemon=True).start()

@app.get("/health", response_model=SystemSnapshot)
def health_check():
    return collect_system_data()
