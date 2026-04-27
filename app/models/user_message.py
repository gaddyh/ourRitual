from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field


class UserMessage(BaseModel):
    message_id: str
    user_id: str
    relationship_id: str
    session_id: str

    input_type: Literal["text", "audio"]
    text: str  # raw text or audio transcript
    timestamp: datetime

    source_context: Literal[
        "free_chat",
        "daily_checkin",
        "pathway_exercise",
        "post_session_followup",
        "pre_session_reflection",
    ] = "free_chat"

    user_reported_intensity: int | None = Field(
        default=None,
        ge=1,
        le=10,
        description="User-reported emotional intensity, 1-10"
    )

    running_avg_intensity_7d: float | None = Field(
        default=None,
        ge=1,
        le=10
    )

    days_since_last_session: int | None = Field(default=None, ge=0)
    days_until_next_session: int | None = Field(default=None, ge=0)

    location_context: Literal[
        "home",
        "work",
        "travel",
        "unknown"
    ] | None = None
