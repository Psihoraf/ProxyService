import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, APIRouter
from pathlib import Path
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
from fastapi.openapi.docs import get_swagger_ui_html

from init import redis_manager

sys.path.append(str(Path(__file__).parent.parent))
from src.api.auth import router as router_auth

@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")
    yield
    await redis_manager.close()

app = FastAPI(lifespan = lifespan)

app.include_router(router_auth)

app.include_router(router_auth)



@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )
if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)