import asyncio
from typing import Optional

from core.agent_base import SoftwareAgent
from shared.domain.entities import SystemSettings
from shared.infrastructure.repositories import InMemoryRepository
from shared.application.services.training_service import TrainingService

class RetrainingAgentRunner(SoftwareAgent[int, str]):
    """
    Agent responsible for Lifecycle & Learning.
    Sense -> Check feedback count
    Think -> Should we retrain?
    Act -> Trigger training
    Learn -> Update system state
    """
    
    def __init__(self, repository: InMemoryRepository, service: TrainingService):
        super().__init__(name="RetrainingAgent")
        self.repo = repository
        self.service = service
        self.settings = SystemSettings() # Should load from DB/File

    async def sense(self) -> Optional[int]:
        # SENSE: How many feedback items do we have?
        all_feedback = self.repo.get_all_feedback()
        count = len(all_feedback)
        
        # Optimization: Don't return anything if count is 0
        if count == 0:
            return None
            
        print(f"[{self.name}] Sensed {count} feedback items.")
        return count

    async def think(self, feedback_count: int) -> Optional[str]:
        # THINK: Is it time to retrain?
        threshold = self.settings.retraining_threshold_count
        
        if feedback_count >= threshold:
            print(f"[{self.name}] Threshold reached ({feedback_count} >= {threshold}). Deciding to RETRAIN.")
            return "START_TRAINING"
        
        return None

    async def act(self, action: str) -> None:
        if action == "START_TRAINING":
            # ACT: Perform the training
            print(f"[{self.name}] Starting training process...")
            new_version = self.service.retrain_model()
            print(f"[{self.name}] Training Complete. New model: {new_version}")
            
            # Update settings
            self.settings.active_model_version = new_version
            
            # Reset feedback (mock logic - in reality we might mark them as 'used')
            # self.repo.clear_feedback() # Implementation detail
            
            # Simulate effort
            await asyncio.sleep(5)

    async def run_forever(self):
        print(f"[{self.name}] Started monitoring for feedback.")
        while True:
            await self.tick()
            # Check less frequently than scoring
            await asyncio.sleep(10)
