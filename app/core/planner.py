from app.models.user_message import UserMessage
from app.models.safety import SafetyResult, SafetyContext
from app.models.intent import IntentEmotionResult
from app.models.retrieved import RetrievedContext
from app.models.plan import ResponsePlan


def create_response_plan(
    message: UserMessage,
    safety_result: SafetyResult,
    intent_result: IntentEmotionResult,
    retrieved_context: RetrievedContext,
) -> ResponsePlan:
    return ResponsePlan(
        mode="emotional_validation",
        objective="Validate user's emotions and provide support",
        key_context_to_use=[],
        constraints=[],
        should_include_exercise=False,
        should_include_content_link=False,
        should_escalate_to_human=False,
        rationale="Mock normal response plan",
    )


def create_safety_response_plan(
    message: UserMessage,
    safety_result: SafetyResult,
    safety_context: SafetyContext | None,
) -> ResponsePlan:
    return ResponsePlan(
        mode="crisis_response",
        objective="Provide crisis resources and support",
        key_context_to_use=[],
        constraints=[],
        should_include_exercise=False,
        should_include_content_link=False,
        should_escalate_to_human=safety_result.needs_human_review,
        rationale="Mock safety response plan",
    )
