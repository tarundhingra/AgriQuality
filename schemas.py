from pydantic import BaseModel, Field
from typing import Literal, List

class QualityDecision(BaseModel):
    recommendation: Literal["ACCEPT", "REJECT", "RETEST"] = Field(description="The final decision for the lot.")
    risk_level: Literal["LOW", "MEDIUM", "HIGH"] = Field(description="Risk assessment based on data.")
    reasons: List[str] = Field(description="Bullet points explaining the decision.")
    evidence: List[str] = Field(description="Evidence retrieved from RAG or Supplier History.")
    next_action: str = Field(description="Specific actionable next step for the executive.")