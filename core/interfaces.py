from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Any

# Generic Types for Agent Components
TPercept = TypeVar('TPercept')       # Inputs (e.g., Evaluation Request)
TAction = TypeVar('TAction')         # Outputs (e.g., Prediction)
TExperience = TypeVar('TExperience') # Learning Data (e.g., Feedback)

class IPerceptionSource(ABC, Generic[TPercept]):
    @abstractmethod
    async def get_next_percept(self) -> Optional[TPercept]:
        """Sense: Retrieve the next item to process."""
        pass

class IActuator(ABC, Generic[TAction]):
    @abstractmethod
    async def perform_action(self, action: TAction) -> None:
        """Act: Execute the decision in the real world."""
        pass

class ILearningComponent(ABC, Generic[TExperience]):
    @abstractmethod
    async def learn(self, experience: TExperience) -> None:
        """Learn: Update internal state based on experience."""
        pass

class IPredictionModel(ABC):
    @abstractmethod
    def predict(self, input_data: Any) -> float:
        """Make a prediction based on input."""
        pass

    @abstractmethod
    def train(self, training_data: Any) -> Any:
        """Train the model."""
        pass

class IRepository(ABC, Generic[TPercept]):
    @abstractmethod
    def save(self, item: TPercept) -> None:
        pass
    
    @abstractmethod
    def get(self, id: str) -> Optional[TPercept]:
        pass
