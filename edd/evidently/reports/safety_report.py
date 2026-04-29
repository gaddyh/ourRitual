from typing import Optional

from evidently import Dataset, DataDefinition, Report
from evidently.core.report import Context
from evidently.core.metric_types import (
    SingleValue,
    SingleValueMetric,
    SingleValueCalculation,
)


class SafetyTotalCostMetric(SingleValueMetric):
    column: str = "safety_error_cost"


class SafetyTotalCostCalculation(SingleValueCalculation[SafetyTotalCostMetric]):
    def calculate(
        self,
        context: Context,
        current_data: Dataset,
        reference_data: Optional[Dataset],
    ) -> SingleValue:
        values = current_data.column(self.metric.column).data
        return self.result(value=float(values.sum()))

    def display_name(self) -> str:
        return "Safety total business cost"


class SafetyAverageCostMetric(SingleValueMetric):
    column: str = "safety_error_cost"


class SafetyAverageCostCalculation(SingleValueCalculation[SafetyAverageCostMetric]):
    def calculate(
        self,
        context: Context,
        current_data: Dataset,
        reference_data: Optional[Dataset],
    ) -> SingleValue:
        values = current_data.column(self.metric.column).data
        return self.result(value=float(values.mean()))

    def display_name(self) -> str:
        return "Safety average business cost"


class MissedCrisisRateMetric(SingleValueMetric):
    column: str = "missed_crisis"


class MissedCrisisRateCalculation(SingleValueCalculation[MissedCrisisRateMetric]):
    def calculate(
        self,
        context: Context,
        current_data: Dataset,
        reference_data: Optional[Dataset],
    ) -> SingleValue:
        values = current_data.column(self.metric.column).data
        return self.result(value=float(values.mean()))

    def display_name(self) -> str:
        return "Missed crisis rate"


class MissedAbuseRateMetric(SingleValueMetric):
    column: str = "missed_abuse"


class MissedAbuseRateCalculation(SingleValueCalculation[MissedAbuseRateMetric]):
    def calculate(
        self,
        context: Context,
        current_data: Dataset,
        reference_data: Optional[Dataset],
    ) -> SingleValue:
        values = current_data.column(self.metric.column).data
        return self.result(value=float(values.mean()))

    def display_name(self) -> str:
        return "Missed abuse rate"


def build_safety_dataset(df) -> Dataset:
    return Dataset.from_pandas(
        df,
        data_definition=DataDefinition(
            id_column="case_id",
            categorical_columns=[
                "expected_safety_action",
                "actual_safety_action",
                "missed_crisis",
                "missed_abuse",
            ],
            numerical_columns=[
                "safety_error_cost",
            ],
        ),
    )


def build_safety_report() -> Report:
    return Report(
        [
            SafetyTotalCostMetric(),
            SafetyAverageCostMetric(),
            MissedCrisisRateMetric(),
            MissedAbuseRateMetric(),
        ],
        tags=[
            "relationship_ai",
            "eval_v1",
            "component:safety",
            "metric:business_cost",
        ],
    )