import uvicorn
from fastapi import FastAPI

from .routers import agent_router

app = FastAPI(
    title='TWON API',
    description="ToDo",
    version="0.0.1",
)

for routers in [
    agent_router
]:
    app.include_router(routers)

if __name__ == "__main__":
    uvicorn.run(app, port=8000, log_level="info")
