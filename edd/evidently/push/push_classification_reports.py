import os
import pandas as pd

from evidently import Dataset, DataDefinition, Report, MulticlassClassification
from evidently.presets import ClassificationPreset
from evidently.ui.workspace import CloudWorkspace

from edd.runners.run_full_eval import run_eval  # must return structured results
from dotenv import load_dotenv

load_dotenv(".venv/.env")

# ---- CONFIG ----

CLASSIFICATION_TASKS = [
    {
        "name": "safety_action",
        "target": "expected_safety_action",
        "prediction": "actual_safety_action",
    },
    {
        "name": "intent",
        "target": "expected_intent",
        "prediction": "actual_intent",
    },
    {
        "name": "emotion",
        "target": "expected_emotion",
        "prediction": "actual_emotion",
    },
    {
        "name": "response_mode",
        "target": "expected_response_mode",
        "prediction": "actual_response_mode",
    },
]


# ---- BUILD DATA ----

def build_eval_dataframe() -> pd.DataFrame:
    results = run_eval()

    rows = []

    for r in results:
        rows.append({
            "case_id": r.case_id,
            "user_input": r.user_input,

            "expected_safety_action": r.expected.safety_action,
            "actual_safety_action": r.actual.safety_action,

            "expected_intent": r.expected.intent,
            "actual_intent": r.actual.intent,

            "expected_emotion": r.expected.emotion,
            "actual_emotion": r.actual.emotion,

            "expected_response_mode": r.expected.response_mode,
            "actual_response_mode": r.actual.response_mode,

            "expected_should_run_deep_safety": r.expected.should_run_deep_safety,
            "should_run_deep_safety": r.actual.should_run_deep_safety,
            "is_ambiguous": r.actual.is_ambiguous,
        })

    df = pd.DataFrame(rows)

    # enforce string type (important for Evidently multiclass)
    bool_cols = {"should_run_deep_safety", "expected_should_run_deep_safety", "is_ambiguous"}
    for col in df.columns:
        if col != "user_input" and col not in bool_cols:
            df[col] = df[col].astype(str)

    return df


# ---- PUSH ONE REPORT ----

def push_one_report(
    ws: CloudWorkspace,
    project_id: str,
    df: pd.DataFrame,
    task_name: str,
    target_col: str,
    prediction_col: str,
):
    report_df = df[
        ["case_id", "user_input", target_col, prediction_col]
    ].rename(
        columns={
            target_col: "target",
            prediction_col: "prediction",
        }
    )

    dataset = Dataset.from_pandas(
        report_df,
        data_definition=DataDefinition(
            id_column="case_id",
            text_columns=["user_input"],
            categorical_columns=["target", "prediction"],
            classification=[
                MulticlassClassification(
                    target="target",
                    prediction_labels="prediction",
                )
            ],
        ),
    )

    # 🔥 TAGS = key for dashboard separation
    report = Report(
        [ClassificationPreset()],
        tags=[
            "relationship_ai",
            "eval_v1",
            f"head:{task_name}",
        ],
    )

    run = report.run(dataset)

    ws.add_run(
        project_id,
        run,
        include_data=True,
        name=f"{task_name}_eval",
    )

    print(f"✅ pushed {task_name}")


# ---- MAIN ----

def main():
    ws = CloudWorkspace(
        token=os.environ["EVIDENTLY_API_KEY"],
        url="https://app.evidently.cloud",
    )

    project_id = os.environ["EVIDENTLY_PROJECT_ID"]

    df = build_eval_dataframe()

    for task in CLASSIFICATION_TASKS:
        push_one_report(
            ws=ws,
            project_id=project_id,
            df=df,
            task_name=task["name"],
            target_col=task["target"],
            prediction_col=task["prediction"],
        )

    print("\n🎯 Done. Use tags in dashboard:")
    print("  head:safety_action")
    print("  head:intent")
    print("  head:emotion")
    print("  head:response_mode")


if __name__ == "__main__":
    main()