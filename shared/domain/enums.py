from enum import Enum

class AgentStatus(str, Enum):
    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    FAILED = "FAILED"

class PredictionConfidence(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class HouseType(str, Enum):
    APARTMENT = "APARTMENT"
    HOUSE = "HOUSE"
    VILLA = "VILLA"
