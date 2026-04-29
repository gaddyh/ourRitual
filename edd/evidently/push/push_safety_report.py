# edd/evidently/push/push_safety_report.py

import os

from evidently.ui.workspace import CloudWorkspace

from edd.evidently.push.push_classification_reports import build_eval_dataframe
from edd.evidently.descriptors.safety_descriptors import add_safety_descriptors
from edd.evidently.reports.safety_report import (
    build_safety_dataset,
    build_safety_report,
)

from edd.problem.business_costs import cost_config


def push(run):
    # ---- push ----
    ws = CloudWorkspace(
        token=os.environ["EVIDENTLY_API_KEY"],
        url="https://app.evidently.cloud",
    )

    project_id = os.environ["EVIDENTLY_PROJECT_ID"]

    ws.add_run(
        project_id,
        run,
        include_data=True,
        name="safety_business_eval",
    )

    print("✅ pushed safety business report")


if __name__ == "__main__":
    push()