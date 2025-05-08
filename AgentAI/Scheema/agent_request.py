from pydantic import BaseModel


# === Request Schema ===
class AgentRequest(BaseModel):
    instruction: str