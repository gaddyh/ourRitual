from pydantic import BaseModel, Field

class ConversationEvaluation(BaseModel):
    session_id: str
    user_id: str
    relationship_id: str

    evaluated_after_turns: int

    user_reported_helpfulness: int | None = Field(default=None, ge=1, le=5)
    user_reported_intensity_before: int | None = Field(default=None, ge=1, le=10)
    user_reported_intensity_after: int | None = Field(default=None, ge=1, le=10)

    completed_exercise: bool = False
    followed_content_recommendation: bool = False
    asked_followup_question: bool = False
    escalated_to_human: bool = False

    evaluator_score: float | None = Field(default=None, ge=0.0, le=1.0)
    evaluator_notes: str | None = None

    decision_chain_errors: list[str] = []