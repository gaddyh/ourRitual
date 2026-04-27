from app.models.user_message import UserMessage
from app.models.safety import SafetyResult
from app.models.intent import IntentEmotionResult


def classify_intent_emotion(message: UserMessage, safety_result: SafetyResult) -> IntentEmotionResult:
    return IntentEmotionResult(
        intent="vent_emotion",
        intent_confidence=0.8,
        primary_emotion="sadness",
        emotion_intensity=0.7,
        secondary_emotions=["anxiety"],
        target="self",
        ambiguity_score=0.2,
        rationale="Mock intent/emotion classification",
    )
