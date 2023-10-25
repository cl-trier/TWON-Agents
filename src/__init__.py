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
