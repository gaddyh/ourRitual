from typing import Literal
from pydantic import BaseModel, Field

RiskCategory = Literal[
    "self_harm",
    "harm_to_others",
    "domestic_abuse",
    "severe_distress",
    "medical_emergency",
    "none",
]

SafetyAction = Literal[
    "continue_normal",
    "clarify_risk",
    "escalate_to_human",
    "show_crisis_resources",
    "block_response",
]


class SafetySignal(BaseModel):
    category: RiskCategory
    score: float = Field(ge=0.0, le=1.0)
    evidence: list[str] = Field(default_factory=list)


class SafetyResult(BaseModel):
    overall_risk_score: float = Field(ge=0.0, le=1.0)
    highest_risk_category: RiskCategory

    signals: list[SafetySignal]

    recommended_action: SafetyAction
    needs_human_review: bool = False

    rationale: str

class SafetyPrecheckResult(BaseModel):
    risk_score: float = Field(ge=0.0, le=1.0)
    is_ambiguous: bool = False
    suspected_categories: list[RiskCategory] = []
    evidence: list[str] = []

    should_run_deep_safety: bool


class SafetyContextItem(BaseModel):
    content: str
    timestamp: str | None = None
    relevance_score: float = Field(ge=0.0, le=1.0)


class SafetyContext(BaseModel):
    recent_messages: list[SafetyContextItem] = []
    recent_high_risk_events: list[SafetyContextItem] = []
    intensity_trend: list[float] = []  # last N intensities

    therapist_safety_notes: list[SafetyContextItem] = []

    has_support_system: bool | None = None  # optional

    summary: str