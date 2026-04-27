from app.models.user_message import UserMessage
from app.models.safety import SafetyResult
from app.models.intent import IntentEmotionResult
from app.models.retrieved import RetrievedContext
from app.models.plan import ResponsePlan
from app.models.assistant import AssistantResponse


def generate_response(
    message: UserMessage,
    safety_result: SafetyResult,
    intent_result: IntentEmotionResult,
    retrieved_context: RetrievedContext,
    response_plan: ResponsePlan,
) -> AssistantResponse:
    return AssistantResponse(
        message="I hear you, and I'm here to support you.",
        follow_up_question=None,
        suggested_exercise_id=None,
        recommended_content_ids=[],
        escalation_triggered=safety_result.recommended_action != "continue_normal",
        escalation_type="crisis" if safety_result.recommended_action != "continue_normal" else None,
        tone="supportive",
        memory_updates=[],
    )
