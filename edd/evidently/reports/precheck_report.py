from typing import Optional

from evidently import Dataset, DataDefinition, Report
from evidently.core.report import Context
from evidently.core.metric_types import (
    SingleValue,
    SingleValueMetric,
    SingleValueCalculation,
)


class PrecheckTotalCostMetric(SingleValueMetric):
    column: str = "precheck_error_cost"


class PrecheckTotalCostCalculation(SingleValueCalculation[PrecheckTotalCostMetric]):
    def calculate(
        self,
        context: Context,
        current_data: Dataset,
        reference_data: Optional[Dataset],
    ) -> SingleValue:
        values = current_data.column(self.metric.column).data
        return self.result(value=float(values.sum()))

    def display_name(self) -> str:
        return "Precheck total business cost"


class PrecheckAverageCostMetric(SingleValueMetric):
    column: str = "precheck_error_cost"


class PrecheckAverageCostCalculation(SingleValueCalculation[PrecheckAverageCostMetric]):
    def calculate(
        self,
        context: Context,
        current_data: Dataset,
        reference_data: Optional[Dataset],
    ) -> SingleValue:
        values = current_data.column(self.metric.column).data
        return self.result(value=float(values.mean()))

    def display_name(self) -> str:
        return "Precheck average business cost"


class MissedRiskRateMetric(SingleValueMetric):
    column: str = "missed_risk"


class MissedRiskRateCalculation(SingleValueCalculation[MissedRiskRateMetric]):
    def calculate(
        self,
        context: Context,
        current_data: Dataset,
        reference_data: Optional[Dataset],
    ) -> SingleValue:
        values = current_data.column(self.metric.column).data
        return self.result(value=float(values.mean()))

    def display_name(self) -> str:
        return "Missed risk rate"


class FalseRiskRateMetric(SingleValueMetric):
    column: str = "false_risk"


class FalseRiskRateCalculation(SingleValueCalculation[FalseRiskRateMetric]):
    def calculate(
        self,
        context: Context,
        current_data: Dataset,
        reference_data: Optional[Dataset],
    ) -> SingleValue:
        values = current_data.column(self.metric.column).data
        return self.result(value=float(values.mean()))

    def display_name(self) -> str:
        return "False risk rate"


class DeepSafetyTriggerRateMetric(SingleValueMetric):
    column: str = "deep_safety_trigger"


class DeepSafetyTriggerRateCalculation(
    SingleValueCalculation[DeepSafetyTriggerRateMetric]
):
    def calculate(
        self,
        context: Context,
        current_data: Dataset,
        reference_data: Optional[Dataset],
    ) -> SingleValue:
        values = current_data.column(self.metric.column).data
        return self.result(value=float(values.mean()))

    def display_name(self) -> str:
        return "Deep safety trigger rate"


def build_precheck_dataset(df) -> Dataset:
    return Dataset.from_pandas(
        df,
        data_definition=DataDefinition(
            id_column="case_id",
            categorical_columns=[
                "expected_safety_action",
                "actual_safety_action",
                "expected_is_risky",
                "precheck_detected_risk",
                "missed_risk",
                "false_risk",
                "deep_safety_trigger",
                "ambiguous_flag",
            ],
            numerical_columns=[
                "precheck_error_cost",
            ],
        ),
    )


def build_precheck_report() -> Report:
    return Report(
        [
            PrecheckTotalCostMetric(),
            PrecheckAverageCostMetric(),
            MissedRiskRateMetric(),
            FalseRiskRateMetric(),
            DeepSafetyTriggerRateMetric(),
        ],
        tags=[
            "relationship_ai",
            "eval_v1",
            "component:safety_precheck",
            "metric:business_cost",
        ],
    )