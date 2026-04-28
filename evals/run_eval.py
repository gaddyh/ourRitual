# evals/run_eval.py

import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from app.models.user_message import UserMessage
from app.core.pipeline import run_assistant_pipeline


@dataclass
class ExpectedResult:
    safety_action: str | None = None
    intent: str | None = None
    emotion: str | None = None
    response_mode: str | None = None


@dataclass
class ActualResult:
    safety_action: str | None = None
    intent: str | None = None
    emotion: str | None = None
    response_mode: str | None = None


@dataclass
class EvalCaseResult:
    case_id: str
    user_input: str
    expected: ExpectedResult
    actual: ActualResult
    passed: bool
    field_results: list = field(default_factory=list)


def load_test_cases(path: str):
    with open(path, "r") as f:
        return json.load(f)


def build_message(input_text: str, case_id: str) -> UserMessage:
    now = datetime.now(UTC)

    return UserMessage(
        message_id=case_id,
        user_id="eval_user",
        relationship_id="eval_rel",
        session_id="eval_session",
        input_type="text",
        text=input_text,
        timestamp=now,
    )


def evaluate_case(case, log) -> EvalCaseResult:
    field_results = []

    expected = ExpectedResult(
        safety_action=case.get("expected_safety_action"),
        intent=case.get("expected_intent"),
        emotion=case.get("expected_emotion"),
        response_mode=case.get("expected_response_mode"),
    )

    actual = ActualResult(
        safety_action=log.safety_result.recommended_action,
        intent=log.intent_emotion_result.intent,
        emotion=log.intent_emotion_result.primary_emotion,
        response_mode=log.response_plan.mode,
    )

    # Safety
    field_results.append(("safety_action", expected.safety_action, actual.safety_action,
                           expected.safety_action == actual.safety_action))

    # Intent
    if expected.intent is not None:
        field_results.append(("intent", expected.intent, actual.intent,
                               expected.intent == actual.intent))

    # Emotion
    if expected.emotion is not None:
        field_results.append(("emotion", expected.emotion, actual.emotion,
                               expected.emotion == actual.emotion))

    # Response mode
    if expected.response_mode is not None:
        field_results.append(("response_mode", expected.response_mode, actual.response_mode,
                               expected.response_mode == actual.response_mode))

    case_pass = all(r[3] for r in field_results)

    return EvalCaseResult(
        case_id=case["case_id"],
        user_input=case["input_text"],
        expected=expected,
        actual=actual,
        passed=case_pass,
        field_results=field_results,
    )


def run_eval() -> list[EvalCaseResult]:
    cases = load_test_cases("app/data/test_cases.json")

    all_results = []
    passed = 0

    for case in cases:
        message = build_message(case["input_text"], case["case_id"])
        log = run_assistant_pipeline(message)

        result = evaluate_case(case, log)
        all_results.append(result)

        print(f"\n=== Case: {result.case_id} ===")
        for name, expected, actual, ok in result.field_results:
            status = "PASS" if ok else "FAIL"
            print(f"{name}: {status} | expected={expected} actual={actual}")

        if result.passed:
            passed += 1
        else:
            print("❌ Case FAILED")

    print("\n=== Summary ===")
    print(f"{passed}/{len(all_results)} passed")

    return all_results


if __name__ == "__main__":
    run_eval()