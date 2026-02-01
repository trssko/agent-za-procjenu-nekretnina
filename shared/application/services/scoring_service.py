from core.interfaces import IPredictionModel
from shared.domain.entities import HouseRequest, PredictionResult, PredictionConfidence
from shared.domain.enums import AgentStatus

class ScoringService:
    def __init__(self, model: IPredictionModel):
        self.model = model

    def score_request(self, request: HouseRequest) -> PredictionResult:
        # THINK: 1. Predict Price
        estimated_price = self.model.predict(request)
        
        # THINK: 2. Apply Confidence Rules (Heuristics)
        confidence = PredictionConfidence.HIGH
        warnings = []
        
        # Rule 1: Extreme area check
        if request.area > 15000:
            confidence = PredictionConfidence.LOW
            warnings.append("Površina je neobično velika (odstupanje). Procjena može biti neprecizna.")
            
        # Rule 2: Minimum Requirements
        if request.bedrooms == 0:
            confidence = PredictionConfidence.LOW
            warnings.append("Kuća ima 0 spavaćih soba. Podaci možda nisu validni.")
            
        return PredictionResult(
            request_id=request.id,
            estimated_price=round(estimated_price, 2),
            confidence=confidence,
            rule_generated_warnings=warnings
        )
