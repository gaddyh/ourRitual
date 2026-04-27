from app.models.user_message import UserMessage
from app.models.safety import SafetyContext, SafetyPrecheckResult, SafetyResult

def run_safety_precheck(message: UserMessage) -> SafetyPrecheckResult:
    text = message.text.lower()

    if any(x in text for x in ["kill myself", "end it", "can't go on"]):
        return SafetyPrecheckResult(
            risk_score=0.9,
            is_ambiguous=False,
            suspected_categories=["self_harm"],
            evidence=[message.text],
            should_run_deep_safety=True,
        )

    if "i can't do this anymore" in text:
        return SafetyPrecheckResult(
            risk_score=0.6,
            is_ambiguous=True,
            suspected_categories=["severe_distress"],
            evidence=[message.text],
            should_run_deep_safety=True,
        )

    return SafetyPrecheckResult(
        risk_score=0.1,
        is_ambiguous=False,
        suspected_categories=["none"],
        evidence=[],
        should_run_deep_safety=False,
    )

def run_deep_safety(message: UserMessage, precheck: SafetyPrecheckResult, context:SafetyContext) -> SafetyResult:
    if precheck.risk_score > 0.8:
        action = "show_crisis_resources"
    elif precheck.is_ambiguous:
        action = "clarify_risk"
    else:
        action = "continue_normal"

    return SafetyResult(
        overall_risk_score=precheck.risk_score,
        highest_risk_category=precheck.suspected_categories[0],
        signals=[],
        recommended_action=action,
        needs_human_review=(action != "continue_normal"),
        rationale="Mock deep safety decision",
    )

def create_low_risk_safety_result(precheck: SafetyPrecheckResult) -> SafetyResult:
    return SafetyResult(
        overall_risk_score=precheck.risk_score,
        highest_risk_category="none",
        signals=[],
        recommended_action="continue_normal",
        needs_human_review=False,
        rationale="Low risk precheck",
    )