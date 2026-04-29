import os

from evidently.ui.workspace import CloudWorkspace

from edd.evidently.descriptors.safety_precheck_descriptors import (
    add_precheck_descriptors,
    add_precheck_cost,
)

from edd.evidently.reports.precheck_report import (
    build_precheck_dataset,
    build_precheck_report,
)


def push(run):
    # ---- Push to Evidently Cloud ----
    ws = CloudWorkspace(
        token=os.environ["EVIDENTLY_API_KEY"],
        url="https://app.evidently.cloud",
    )

    project_id = os.environ["EVIDENTLY_PROJECT_ID"]

    ws.add_run(
        project_id,
        run,
        include_data=True,
        name="precheck_business_eval",
    )

    print("✅ pushed precheck business report")
