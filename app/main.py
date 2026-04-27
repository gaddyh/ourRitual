from datetime import datetime
from app.core.pipeline import run_assistant_pipeline
from app.models.user_message import UserMessage

message = UserMessage(
    message_id="msg_001",
    user_id="user_001",
    relationship_id="rel_001",
    session_id="sess_001",
    input_type="text",
    text="I'm feeling really down today",
    timestamp=datetime.now(),
)

result = run_assistant_pipeline(message)
print(f"Response: {result.assistant_response.message}")
