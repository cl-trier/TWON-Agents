from fastapi import FastAPI, APIRouter
from fastapi.openapi.docs import (
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles


def create_route(app: FastAPI) -> APIRouter:
    router = APIRouter()

    app.mount("/static", StaticFiles(directory="static"), name="static")

    @router.get("/")
    async def redirect_to_docs():
        """
        The route redirects the API root to the Swagger API documentation page.
        """
        return RedirectResponse(url='/docs')

    @router.get("/docs")
    async def swagger_docs():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
            swagger_css_url="/static/swagger-ui.css",
        )

    @router.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    return router
