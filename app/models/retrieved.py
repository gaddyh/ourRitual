from pydantic import BaseModel, Field
from typing import Literal


class ContextItem(BaseModel):
    source_type: str
    title: str | None = None
    content: str
    relevance_score: float = Field(ge=0.0, le=1.0)
    timestamp: str | None = None


class RetrievedContext(BaseModel):
    user_state: list[ContextItem] = []
    partner_context: list[ContextItem] = []
    therapist_guidance: list[ContextItem] = []
    pathway_progress: list[ContextItem] = []
    retrieved_content: list[ContextItem] = []

    retrieval_summary: str
    missing_context: list[str] = []

    permission_level: Literal["user_only", "partner_shared", "therapist_approved"]