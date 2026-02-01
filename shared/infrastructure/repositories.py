from typing import List, Optional, Dict, Any
from core.interfaces import IRepository
from shared.domain.entities import HouseRequest, PredictionResult, Feedback

class InMemoryRepository(IRepository):
    """
    Simple in-memory storage for testing without DB.
    In production, this would be SQLAlchemy or similar.
    """
    def __init__(self):
        self._requests: Dict[str, HouseRequest] = {}
        self._predictions: Dict[str, PredictionResult] = {}
        self._feedback: List[Feedback] = []

    def save(self, item: Any) -> None:
        # Generic save implementation routing by type
        if isinstance(item, HouseRequest):
            self.save_request(item)
        elif isinstance(item, PredictionResult):
            self.save_prediction(item)
        elif isinstance(item, Feedback):
            self.save_feedback(item)
            
    def get(self, id: str) -> Optional[Any]:
        # Generic get - try request first, then prediction
        # (In a real app, strict typing would prevent this ambiguity)
        req = self.get_request(id)
        if req: return req
        pred = self.get_prediction(id)
        if pred: return pred
        return None

    def save_request(self, item: HouseRequest) -> None:
        self._requests[item.id] = item

    def get_request(self, id: str) -> Optional[HouseRequest]:
        return self._requests.get(id)
    
    def get_pending_requests(self) -> List[HouseRequest]:
        return [r for r in self._requests.values() if r.status == "QUEUED"]
    
    def save_prediction(self, item: PredictionResult) -> None:
        self._predictions[item.request_id] = item
        
    def get_prediction(self, request_id: str) -> Optional[PredictionResult]:
        return self._predictions.get(request_id)

    def save_feedback(self, item: Feedback) -> None:
        self._feedback.append(item)
    
    def get_all_feedback(self) -> List[Feedback]:
        return self._feedback
