from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional
from .interfaces import IPerceptionSource, IActuator

TPercept = TypeVar('TPercept')
TAction = TypeVar('TAction')

class SoftwareAgent(ABC, Generic[TPercept, TAction]):
    """
    Base class for specific agents (Runners).
    Implements the Sense -> Think -> Act loop boilerplate.
    """

    def __init__(self, name: str):
        self.name = name

    async def tick(self):
        """
        One atomic step of the agent's lifecycle.
        Should be calling constantly by the Host.
        """
        # 1. SENSE
        percept = await self.sense()
        if percept is None:
            return None # No work to do

        # 2. THINK
        action = await self.think(percept)
        
        # 3. ACT
        if action:
            await self.act(action)
        
        # 4. LEARN (Optional hook)
        await self.learn_hook(percept, action)
        
        return "Ticked"

    @abstractmethod
    async def sense(self) -> Optional[TPercept]:
        """Retrieve state from the environment."""
        pass

    @abstractmethod
    async def think(self, percept: TPercept) -> Optional[TAction]:
        """Process perception and decide on an action."""
        pass

    @abstractmethod
    async def act(self, action: TAction) -> None:
        """Execute the action."""
        pass
    
    async def learn_hook(self, percept: TPercept, action: TAction) -> None:
        """Optional override for learning agents."""
        pass
