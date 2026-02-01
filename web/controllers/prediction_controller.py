from fastapi import APIRouter, HTTPException
from shared.domain.entities import HouseRequest, Feedback
from shared.infrastructure.repositories import InMemoryRepository

# Note: In a real app, use Dependency Injection to get the repo
# For now we import the singleton from main (circular import risk in real apps, 
# but we'll cheat slightly for this structural demo by assuming shared access or passing it)
# To keep it clean, we'll instantiate a repo instance here, 
# BUT CAUTION: InMemoryRepository creates new dicts! 
# We need the SAME instance.
# FIX: Refactor main.py to expose the repo or use app.state.

router = APIRouter()

@router.post("/predict")
async def request_prediction(request: HouseRequest):
    """
    Client sends request -> We queue it -> Agent picks it up later.
    This is async communication conformant to Agent specs.
    """
    from web.container import repo 
    
    repo.save_request(request)
    
    return {"message": "Request Queued", "request_id": request.id, "status": "QUEUED"}

@router.get("/status/{request_id}")
async def get_status(request_id: str):
    from web.container import repo
    
    # Check prediction first
    prediction = repo.get_prediction(request_id)
    if prediction:
        return {"status": "COMPLETED", "result": prediction}
    
    # Check request logic
    req = repo.get_request(request_id)
    if not req:
        raise HTTPException(status_code=404, detail="Request not found")
        
    return {"status": req.status, "result": None}

@router.post("/feedback")
async def submit_feedback(feedback: Feedback):
    from web.container import repo
    repo.save_feedback(feedback)
    return {"message": "Feedback received. Agent may retrain."}
