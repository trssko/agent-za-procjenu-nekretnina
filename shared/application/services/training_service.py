from core.interfaces import IPredictionModel, IRepository

class TrainingService:
    def __init__(self, model: IPredictionModel, repository: IRepository):
        self.model = model
        self.repo = repository

    def retrain_model(self) -> str:
        """
        Gathers data and retrains the model.
        Returns the new model version ID.
        """
        # 1. Gather Data (Feedback + Historical)
        feedback_data = self.repo.get_all_feedback()
        
        # 2. Train
        # In real scenario, we merge original data with new feedback
        new_version = self.model.train(feedback_data)
        
        return new_version
