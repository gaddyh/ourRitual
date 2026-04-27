# evals/run_eval.py

import json
from datetime import UTC, datetime
from app.models.user_message import UserMessage
from app.core.pipeline import run_assistant_pipeline


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

def evaluate_case(case, log):
    results = []

    # Safety
    expected = case.get("expected_safety_action")
    actual = log.safety_result.recommended_action
    results.append(("safety_action", expected, actual, expected == actual))

    # Intent
    if "expected_intent" in case:
        expected = case["expected_intent"]
        actual = log.intent_emotion_result.intent
        results.append(("intent", expected, actual, expected == actual))

    # Emotion
    if "expected_emotion" in case:
        expected = case["expected_emotion"]
        actual = log.intent_emotion_result.primary_emotion
        results.append(("emotion", expected, actual, expected == actual))

    # Response mode
    if "expected_response_mode" in case:
        expected = case["expected_response_mode"]
        actual = log.response_plan.mode
        results.append(("response_mode", expected, actual, expected == actual))

    return results

def run_eval():
    cases = load_test_cases("app/data/test_cases.json")

    total = 0
    passed = 0

    for case in cases:
        total += 1

        message = build_message(case["input_text"], case["case_id"])
        log = run_assistant_pipeline(message)

        results = evaluate_case(case, log)

        case_pass = all(r[3] for r in results)

        print(f"\n=== Case: {case['case_id']} ===")

        for name, expected, actual, ok in results:
            status = "PASS" if ok else "FAIL"
            print(f"{name}: {status} | expected={expected} actual={actual}")

        if case_pass:
            passed += 1
        else:
            print("❌ Case FAILED")

    print("\n=== Summary ===")
    print(f"{passed}/{total} passed")


if __name__ == "__main__":
    run_eval()