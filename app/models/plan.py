from typing import Literal
from pydantic import BaseModel, Field


ResponseMode = Literal[
    "clarifying_question",
    "crisis_response",
    "emotional_validation",
    "guided_reflection",
    "coping_exercise",
    "communication_script",
    "content_recommendation",
]


class ResponsePlan(BaseModel):
    mode: ResponseMode

    objective: str
    key_context_to_use: list[str] = []
    constraints: list[str] = []

    should_include_exercise: bool = False
    should_include_content_link: bool = False
    should_escalate_to_human: bool = False

    rationale: str