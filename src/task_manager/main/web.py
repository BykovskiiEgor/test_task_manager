import logging
import os

import uvicorn
from fastapi import FastAPI

from task_manager.adapters.fapi.index import index_router
from task_manager.adapters.fapi.tasks.routers import task_router

logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    app = FastAPI()
    init_routers(app)
    return app

def init_routers(app: FastAPI) -> None:
    app.include_router(index_router)
    app.include_router(task_router)


async def run_api(app: FastAPI) -> None:
    config = uvicorn.Config(
        app,
        host=os.getenv('host'),
        port=8000,
        log_level=logging.INFO,
    )

    server = uvicorn.Server(config)
    logger.info('Server started')
    await server.serve()
