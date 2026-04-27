
from pydantic import BaseModel
from datetime import datetime
from .user_message import UserMessage
from .safety import SafetyResult
from .intent import IntentEmotionResult
from .retrieved import RetrievedContext
from .plan import ResponsePlan
from .assistant import AssistantResponse

class InteractionLog(BaseModel):
    interaction_id: str
    user_id: str
    relationship_id: str
    session_id: str
    timestamp: datetime

    user_message: UserMessage
    safety_result: SafetyResult
    intent_emotion_result: IntentEmotionResult
    retrieved_context: RetrievedContext
    response_plan: ResponsePlan
    assistant_response: AssistantResponse

    model_name: str
    prompt_version: str
    pipeline_version: str