from shared.infrastructure.repositories import InMemoryRepository
from shared.ml.mock_model import MockXGBoostModel
from shared.application.services.scoring_service import ScoringService
from shared.application.services.training_service import TrainingService
from shared.application.runners.scoring_runner import ScoringAgentRunner
from shared.application.runners.retraining_runner import RetrainingAgentRunner

# Initialize Singletons
repo = InMemoryRepository()
model = MockXGBoostModel()

scoring_service = ScoringService(model)
training_service = TrainingService(model, repo)

scoring_agent = ScoringAgentRunner(repo, scoring_service)
retraining_agent = RetrainingAgentRunner(repo, training_service)
