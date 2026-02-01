import asyncio
from typing import Optional

from core.agent_base import SoftwareAgent
from shared.domain.entities import HouseRequest, PredictionResult
from shared.domain.enums import AgentStatus
from shared.infrastructure.repositories import InMemoryRepository
from shared.application.services.scoring_service import ScoringService

class ScoringAgentRunner(SoftwareAgent[HouseRequest, PredictionResult]):
    """
    The main agent loop for processing new requests.
    Sense -> Repo (Get Queue)
    Think -> Service (Predict)
    Act -> Repo (Save)
    """
    
    def __init__(self, repository: InMemoryRepository, service: ScoringService):
        super().__init__(name="HousingScoringAgent")
        self.repo = repository
        self.service = service

    async def sense(self) -> Optional[HouseRequest]:
        # SENSE: Check if there are any pending requests in the queue
        pending = self.repo.get_pending_requests()
        if pending:
            # Pick the first one (FIFO)
            # In a real DB we would lock this row
            request = pending[0]
            print(f"[{self.name}] Sensed new request: {request.id}")
            return request
        return None

    async def think(self, percept: HouseRequest) -> Optional[PredictionResult]:
        # THINK: Use the service to apply intelligence
        # First mark as processing so other workers don't pick it (if we had concurrency)
        percept.status = AgentStatus.PROCESSING
        self.repo.save_request(percept)
        
        print(f"[{self.name}] Thinking about request for {percept.area} sqft...")
        
        # Simulate thinking time (to make it feel like an agent)
        await asyncio.sleep(2) 
        
        result = self.service.score_request(percept)
        return result

    async def act(self, action: PredictionResult) -> None:
        # ACT: Persist the decision
        print(f"[{self.name}] Acting: Estimated {action.estimated_price}")
        
        self.repo.save_prediction(action)
        
        # Update the request status
        request = self.repo.get_request(action.request_id)
        if request:
            request.status = AgentStatus.COMPLETED
            self.repo.save_request(request)
            
    async def run_forever(self):
        print(f"[{self.name}] Started.")
        while True:
            await self.tick()
            # Wait a bit before next tick to avoid CPU spinning when idle
            await asyncio.sleep(1)
