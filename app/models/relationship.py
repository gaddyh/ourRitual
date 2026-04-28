# app/models/relationship.py

from pydantic import BaseModel, Field
from typing import Literal


ConflictType = Literal[
    "emotional_distance",
    "communication_breakdown",
    "trust_issue",
    "repeated_argument",
    "unmet_need",
    "jealousy",
    "parenting_conflict",
    "intimacy_issue",
    "unclear",
]


AttachmentSignal = Literal[
    "seeking_reassurance",
    "fear_of_abandonment",
    "avoidance",
    "pursuit_withdrawal",
    "self_protection",
    "none_detected",
]


class RelationshipAssessment(BaseModel):
    conflict_type: ConflictType
    attachment_signal: AttachmentSignal

    relationship_dynamic: str
    user_position: str
    partner_position_inferred: str | None = None

    core_unmet_need: str | None = None
    likely_conversation_risk: str | None = None

    confidence: float = Field(ge=0.0, le=1.0)
    evidence: list[str] = []