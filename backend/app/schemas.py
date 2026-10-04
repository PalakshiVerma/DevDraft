from enum import Enum
from pydantic import BaseModel, Field


class TaskType(str, Enum):
    STANDUP = "standup"
    PR = "pr"


class PolishRequest(BaseModel):
    raw_text: str = Field(
        ...,
        min_length=5,
        max_length=5000,
        description="Raw, informal notes from the developer",
        examples=["i fixed the login bug but css is still weird so didnt push that part"]
    )
    task_type: TaskType = Field(
        default=TaskType.STANDUP,
        description="Type of polish required: 'standup' or 'pr'"
    )


class PolishResponse(BaseModel):
    polished_text: str = Field(
        ...,
        description="Polished, professional, senior-developer formatted update"
    )
    task_type: TaskType
    model_used: str = Field(
        ...,
        description="The actual LLM model used for inference (set from LLM_MODEL env var)"
    )


class HealthResponse(BaseModel):
    status: str
    llm_configured: bool
    version: str = "1.0.0"
