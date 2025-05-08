from fastapi import FastAPI, HTTPException
import uvicorn
import requests
import json
from Routers.todo_router import router as todo_router
from Scheema.agent_request import AgentRequest



# === Define FastAPI ===
app = FastAPI(title="Todo Agent API")




# === Routers ===
app.include_router(todo_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)