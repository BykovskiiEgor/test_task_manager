import asyncio

from task_manager.main.web import create_app, run_api
from task_manager.adapters.db.connection import init_models

async def main():
    await init_models()
    app = create_app()
    await run_api(app)

if __name__ == "__main__":
    asyncio.run(main())