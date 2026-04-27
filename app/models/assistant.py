from typing import List, Optional
from pydantic import BaseModel


class MemoryUpdate(BaseModel):
    key: str
    value: str
    importance: float  # 0–1
    source: str  # "inferred", "user_stated", "therapist_note"


class AssistantResponse(BaseModel):
    message: str  # main response text

    follow_up_question: Optional[str] = None

    suggested_exercise_id: Optional[str] = None
    recommended_content_ids: List[str] = []

    escalation_triggered: bool = False
    escalation_type: Optional[str] = None  # "crisis", "therapist_followup"

    tone: Optional[str] = None  # "supportive", "direct", "calm"

    memory_updates: List[MemoryUpdate] = []