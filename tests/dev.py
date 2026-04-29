import pandas as pd

from edd.evidently.push.push_classification_reports import build_eval_dataframe
from edd.evidently.descriptors.safety_precheck_descriptors import add_precheck_descriptors, add_precheck_cost
from edd.problem.business_costs import cost_config
from edd.evidently.reports.precheck_report import build_precheck_dataset, build_precheck_report
from edd.evidently.push.push_precheck_report import push

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

df = build_eval_dataframe()
# ---- Add precheck descriptors ----
df = add_precheck_descriptors(df)

# ---- Add precheck business cost ----
df = add_precheck_cost(df, cost_config)

# ---- Build Evidently dataset ----
dataset = build_precheck_dataset(df)

# ---- Build report ----
report = build_precheck_report()

# ---- Run report ----
run = report.run(dataset)

push(run)
