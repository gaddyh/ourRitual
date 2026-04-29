# edd/evidently/push/push_descriptor_reports.py

import os
import pandas as pd

from evidently import Dataset, DataDefinition, Report
from evidently.presets import TextEvals
from evidently.ui.workspace import CloudWorkspace

from edd.runners.run_full_eval import run_eval
from dotenv import load_dotenv

load_dotenv(".venv/.env")

def build_eval_dataframe():
    results = run_eval()

    rows = []

    for r in results:
        rows.append({
            "case_id": r.case_id,
            "user_input": r.user_input,

            "expected_safety_action": r.expected.safety_action,
            "actual_safety_action": r.actual.safety_action,
            "safety_pass": r.expected.safety_action == r.actual.safety_action,

            "expected_intent": r.expected.intent,
            "actual_intent": r.actual.intent,
            "intent_pass": r.expected.intent == r.actual.intent,

            "expected_emotion": r.expected.emotion,
            "actual_emotion": r.actual.emotion,
            "emotion_pass": r.expected.emotion == r.actual.emotion,

            "expected_response_mode": r.expected.response_mode,
            "actual_response_mode": r.actual.response_mode,
            "response_mode_pass": r.expected.response_mode == r.actual.response_mode,

            "case_pass": r.passed,
        })

    return pd.DataFrame(rows)


def push_to_evidently():
    token = os.environ["EVIDENTLY_API_KEY"]
    project_id = os.environ["EVIDENTLY_PROJECT_ID"]

    ws = CloudWorkspace(
        token=token,
        url="https://app.evidently.cloud",
    )

    project = ws.get_project(project_id)

    df = build_eval_dataframe()

    dataset = Dataset.from_pandas(
        df,
        data_definition=DataDefinition(
            text_columns=["user_input"],
            categorical_columns=[
                "case_id",
                "expected_safety_action",
                "actual_safety_action",
                "expected_intent",
                "actual_intent",
                "expected_emotion",
                "actual_emotion",
                "expected_response_mode",
                "actual_response_mode",
            ],
            numerical_columns=[],
        ),
    )

    report = Report([
        TextEvals(),
    ])

    run = report.run(dataset)

    ws.add_run(
        project.id,
        run,
        include_data=True,
    )

    print("Pushed eval run to Evidently")
    print(f"Rows: {len(df)}")
    print(f"Pass rate: {df['case_pass'].mean():.2%}")


if __name__ == "__main__":
    push_to_evidently()