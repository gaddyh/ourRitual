from typing import Literal
from pydantic import BaseModel, Field


IntentType = Literal[
    "vent_emotion",
    "seek_advice",
    "situation_report",
    "reflect_on_pathway",
    "exercise_submission",
    "unknown",
]

EmotionType = Literal[
    "anger",
    "sadness",
    "anxiety",
    "frustration",
    "hurt",
    "confusion",
    "hope",
    "neutral",
]


TargetType = Literal[
    "partner",
    "self",
    "family",
    "therapist",
    "other",
]


class IntentEmotionResult(BaseModel):
    intent: IntentType
    intent_confidence: float = Field(ge=0.0, le=1.0)

    primary_emotion: EmotionType
    emotion_intensity: float = Field(ge=0.0, le=1.0)

    secondary_emotions: list[EmotionType] = []

    target: TargetType

    ambiguity_score: float = Field(
        ge=0.0,
        le=1.0,
        description="How unclear or mixed the message is"
    )

    rationale: str