from app.models.safety import SafetyContext
from app.models.user_message import UserMessage
from app.models.safety import SafetyResult
from app.models.intent import IntentEmotionResult
from app.models.retrieved import RetrievedContext


def retrieve_safety_context(message, precheck) -> SafetyContext:
    return SafetyContext(
        recent_messages=[],
        recent_high_risk_events=[],
        intensity_trend=[5, 6, 7],
        therapist_safety_notes=[],
        has_support_system=True,
        summary="Mock safety context",
    )


def retrieve_context(
    message: UserMessage,
    safety_result: SafetyResult,
    intent_result: IntentEmotionResult,
) -> RetrievedContext:
    return RetrievedContext(
        user_state=[],
        partner_context=[],
        therapist_guidance=[],
        pathway_progress=[],
        retrieved_content=[],
        retrieval_summary="Mock retrieved context",
        missing_context=[],
        permission_level="user_only",
    )


def create_empty_retrieved_context(summary: str) -> RetrievedContext:
    return RetrievedContext(
        user_state=[],
        partner_context=[],
        therapist_guidance=[],
        pathway_progress=[],
        retrieved_content=[],
        retrieval_summary=summary,
        missing_context=[],
        permission_level="user_only",
    )