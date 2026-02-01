from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from uuid import uuid4
from .enums import AgentStatus, PredictionConfidence

class HouseRequest(BaseModel):
    """
    Represents a user request to evaluate a house.
    This is the 'Percept' for the ScoringAgent.
    """
    id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(default_factory=datetime.now)
    area: float
    bedrooms: int
    bathrooms: int
    stories: int
    mainroad: bool
    guestroom: bool
    basement: bool
    hotwaterheating: bool
    airconditioning: bool
    parking: int
    prefarea: bool
    furnishingstatus: str
    
    # Process State
    status: AgentStatus = AgentStatus.QUEUED

class PredictionResult(BaseModel):
    """
    The output 'Action' of the ScoringAgent.
    """
    request_id: str
    estimated_price: float
    confidence: PredictionConfidence
    rule_generated_warnings: List[str] = []
    generated_at: datetime = Field(default_factory=datetime.now)

class Feedback(BaseModel):
    """
    Represents 'Experience' for the Learning Agent.
    Real sold price provided by user later.
    """
    request_id: str
    actual_price: float
    feedback_at: datetime = Field(default_factory=datetime.now)
    
class SystemSettings(BaseModel):
    """
    Global settings for the agents.
    """
    retraining_enabled: bool = True
    retraining_threshold_count: int = 1
    active_model_version: str = "v1"
