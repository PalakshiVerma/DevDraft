import logging
import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables from .env file if available
load_dotenv()

from app.schemas import PolishRequest, PolishResponse, HealthResponse
from app.services import polish_service

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Standup & PR Polish API",
    description=(
        "Backend service powered by open-weight LLMs (default: Llama 3.1 via Groq) "
        "to convert raw developer notes into professional standup or PR updates. "
        "Provider is fully configurable via LLM_BASE_URL / LLM_API_KEY / LLM_MODEL env vars."
    ),
    version="2.0.0",
)

# CORS — allow all origins for development and cloud (Streamlit Community Cloud)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check: returns server status and whether an LLM API key is configured."""
    return HealthResponse(
        status="healthy",
        llm_configured=polish_service.is_configured(),
        version="2.0.0",
    )


@app.post(
    "/api/polish",
    response_model=PolishResponse,
    status_code=status.HTTP_200_OK,
    tags=["Polish"],
)
async def polish_update_endpoint(request: PolishRequest):
    """
    Transforms raw, informal developer notes into a crisp, confident
    Standup or Pull Request update using an open-weight LLM.
    """
    if not polish_service.is_configured():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="LLM_API_KEY is not configured on the server. Please set it in .env file.",
        )

    try:
        response = await polish_service.polish_update(
            raw_text=request.raw_text,
            task_type=request.task_type,
        )
        return response
    except ValueError as ve:
        # Non-retryable client error (e.g., bad model name, 400/401/403)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except RuntimeError as re:
        # Upstream LLM failure after retries
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=str(re))
    except Exception:
        # Unexpected errors — log server-side, do NOT expose internals to client
        logger.exception("Unexpected error in /api/polish")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected internal server error occurred.",
        )


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
