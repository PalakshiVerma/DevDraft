import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables from .env file if available
load_dotenv()

from app.schemas import PolishRequest, PolishResponse, HealthResponse
from app.services import polish_service

app = FastAPI(
    title="Standup & PR Polish API",
    description="Backend service powered by Google Gemini (gemini-2.5-flash) to convert raw developer notes into professional updates.",
    version="1.0.0",
)

# CORS configuration to allow local & deployed Streamlit frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development and cloud deployments
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint to verify server status and Gemini API key configuration."""
    return HealthResponse(
        status="healthy",
        gemini_configured=polish_service.is_configured(),
        version="1.0.0",
    )


@app.post(
    "/api/polish",
    response_model=PolishResponse,
    status_code=status.HTTP_200_OK,
    tags=["Polish"],
)
async def polish_update_endpoint(request: PolishRequest):
    """
    Transforms raw, informal developer notes into a crisp, confident Standup or Pull Request update.
    """
    if not polish_service.is_configured():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="GEMINI_API_KEY is not configured on the server. Please set it in .env file.",
        )

    try:
        response = await polish_service.polish_update(
            raw_text=request.raw_text,
            task_type=request.task_type,
        )
        return response
    except ValueError as ve:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(ve),
        )
    except RuntimeError as re:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(re),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}",
        )


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)
