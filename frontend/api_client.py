import os
import httpx
from typing import Tuple, Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

DEFAULT_BACKEND_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")


def check_backend_health(base_url: str = DEFAULT_BACKEND_URL) -> Tuple[bool, Optional[str]]:
    """Check if the FastAPI backend is reachable and configured."""
    try:
        url = f"{base_url.rstrip('/')}/health"
        with httpx.Client(timeout=3.0) as client:
            resp = client.get(url)
            if resp.status_code == 200:
                data = resp.json()
                if not data.get("gemini_configured", False):
                    return False, "Backend reachable, but GEMINI_API_KEY is not set."
                return True, "Backend online and ready."
            return False, f"Backend returned status {resp.status_code}"
    except httpx.ConnectError:
        return False, f"Could not connect to backend at {base_url}. Is FastAPI running?"
    except Exception as e:
        return False, f"Health check failed: {str(e)}"


def call_polish_api(
    raw_text: str,
    task_type: str,
    base_url: str = DEFAULT_BACKEND_URL,
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Call the /api/polish endpoint."""
    url = f"{base_url.rstrip('/')}/api/polish"
    payload = {
        "raw_text": raw_text,
        "task_type": task_type,
    }
    try:
        with httpx.Client(timeout=30.0) as client:
            resp = client.post(url, json=payload)
            if resp.status_code == 200:
                return resp.json(), None
            else:
                detail = resp.json().get("detail", resp.text)
                return None, f"Error ({resp.status_code}): {detail}"
    except httpx.ConnectError:
        return None, f"Connection failed to {base_url}. Please ensure the FastAPI backend is running."
    except httpx.TimeoutException:
        return None, "Request timed out while waiting for Gemini response."
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"
