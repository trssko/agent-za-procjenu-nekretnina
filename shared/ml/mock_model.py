from core.interfaces import IPredictionModel
from typing import Any
import random

class MockXGBoostModel(IPredictionModel):
    """
    Temporary mock until we train the real model.
    """
    def predict(self, input_data: Any) -> float:
        # Mock logic tuned for Sarajevo Market (Approx. 2025 prices)
        # Base value for a plot/location
        base_price = 50000 
        
        # Standard price approx 3500 KM/m2 
        # input_data.area is in sqft (from frontend conversion)
        # 3500 KM/m2 / 10.764 = ~325 KM/sqft
        area_factor = input_data.area * 325
        
        # Stories add value (e.g. 15k per extra story)
        stories_factor = input_data.stories * 15000
        
        # Bedrooms
        bedroom_factor = input_data.bedrooms * 10000
        
        noise = random.randint(-5000, 5000)
        return base_price + area_factor + stories_factor + bedroom_factor + noise

    def train(self, training_data: Any) -> Any:
        print("Mock training started...")
        return "mock_model_v2.pkl"
