import asyncio
from fastapi import FastAPI, BackgroundTasks
from contextlib import asynccontextmanager

from web.container import scoring_agent, retraining_agent
from web.controllers import prediction_controller

# Note: Dependencies are initialized in web.container


@asynccontextmanager
async def lifespan(app: FastAPI):
    # STARTUP: Launch Agents in Background
    print("System Startup: Launching Agents...")
    
    # Run agents as background tasks
    loop = asyncio.get_event_loop()
    scoring_task = loop.create_task(scoring_agent.run_forever())
    training_task = loop.create_task(retraining_agent.run_forever())
    
    yield
    
    # SHUTDOWN
    print("System Shutdown: Stopping Agents...")
    scoring_task.cancel()
    training_task.cancel()

app = FastAPI(title="Housing Valuation Agent", lifespan=lifespan)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(prediction_controller.router, prefix="/api", tags=["Prediction"])

@app.get("/")
def home():
    return {"message": "Agent System Online", "status": "Active"}
