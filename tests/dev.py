import pandas as pd

from edd.evidently.push.push_classification_reports import build_eval_dataframe
from edd.evidently.descriptors.safety_precheck_descriptors import add_precheck_descriptors

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

df = build_eval_dataframe()
df = add_precheck_descriptors(df)

print(df)

