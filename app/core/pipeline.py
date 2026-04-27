# core/pipeline.py

from app.models.user_message import UserMessage
from app.models.safety import SafetyResult, SafetyContext
from app.models.intent import IntentEmotionResult
from app.models.retrieved import RetrievedContext
from app.models.plan import ResponsePlan
from app.models.assistant import AssistantResponse
from app.models.log import InteractionLog

from app.core.safety import (
    run_safety_precheck,
    run_deep_safety,
    create_low_risk_safety_result,
)
from app.core.retriever import retrieve_safety_context
from app.core.classifier import classify_intent_emotion
from app.core.retriever import retrieve_context, create_empty_retrieved_context
from app.core.planner import create_response_plan, create_safety_response_plan
from app.core.responder import generate_response


PIPELINE_VERSION = "0.1.0"


def run_assistant_pipeline(message: UserMessage) -> InteractionLog:
    safety_result, safety_context = run_safety_stage(message)

    if safety_result.recommended_action != "continue_normal":
        return run_safety_path(
            message=message,
            safety_result=safety_result,
            safety_context=safety_context,
        )

    return run_normal_path(
        message=message,
        safety_result=safety_result,
    )


def run_safety_stage(
    message: UserMessage,
) -> tuple[SafetyResult, SafetyContext | None]:
    precheck = run_safety_precheck(message)

    if not precheck.should_run_deep_safety:
        return create_low_risk_safety_result(precheck), None

    safety_context = retrieve_safety_context(message, precheck)
    safety_result = run_deep_safety(message, precheck, safety_context)

    return safety_result, safety_context


def run_safety_path(
    message: UserMessage,
    safety_result: SafetyResult,
    safety_context: SafetyContext | None,
) -> InteractionLog:
    intent_result = classify_intent_emotion(message, safety_result)

    retrieved_context = create_empty_retrieved_context(
        summary="Normal retrieval skipped because safety path was triggered."
    )

    response_plan = create_safety_response_plan(
        message=message,
        safety_result=safety_result,
        safety_context=safety_context,
    )

    assistant_response = generate_response(
        message=message,
        safety_result=safety_result,
        intent_result=intent_result,
        retrieved_context=retrieved_context,
        response_plan=response_plan,
    )

    return build_interaction_log(
        message=message,
        safety_result=safety_result,
        intent_result=intent_result,
        retrieved_context=retrieved_context,
        response_plan=response_plan,
        assistant_response=assistant_response,
    )


def run_normal_path(
    message: UserMessage,
    safety_result: SafetyResult,
) -> InteractionLog:
    intent_result = classify_intent_emotion(message, safety_result)

    retrieved_context = retrieve_context(
        message=message,
        safety_result=safety_result,
        intent_result=intent_result,
    )

    response_plan = create_response_plan(
        message=message,
        safety_result=safety_result,
        intent_result=intent_result,
        retrieved_context=retrieved_context,
    )

    assistant_response = generate_response(
        message=message,
        safety_result=safety_result,
        intent_result=intent_result,
        retrieved_context=retrieved_context,
        response_plan=response_plan,
    )

    return build_interaction_log(
        message=message,
        safety_result=safety_result,
        intent_result=intent_result,
        retrieved_context=retrieved_context,
        response_plan=response_plan,
        assistant_response=assistant_response,
    )


def build_interaction_log(
    message: UserMessage,
    safety_result: SafetyResult,
    intent_result: IntentEmotionResult,
    retrieved_context: RetrievedContext,
    response_plan: ResponsePlan,
    assistant_response: AssistantResponse,
) -> InteractionLog:
    return InteractionLog(
        interaction_id=f"int_{message.message_id}",
        user_id=message.user_id,
        relationship_id=message.relationship_id,
        session_id=message.session_id,
        timestamp=message.timestamp,
        user_message=message,
        safety_result=safety_result,
        intent_emotion_result=intent_result,
        retrieved_context=retrieved_context,
        response_plan=response_plan,
        assistant_response=assistant_response,
        model_name="mock-v0",
        prompt_version="none",
        pipeline_version=PIPELINE_VERSION,
    )