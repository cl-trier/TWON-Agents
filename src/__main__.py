import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .auth import auth
from .routers import explicit_agent_router

DOCS: str = './docs'

app = FastAPI(
    title='TWON API',
    description=open(f'{DOCS}/Root.md').read(),
    version="0.0.1",
)


@app.get("/")
async def redirect_docs():
    return RedirectResponse(url='/docs')


for routers in [
    explicit_agent_router
]:
    app.include_router(routers)

auth()

if __name__ == "__main__":
    uvicorn.run(app, port=8000, log_level="info")
