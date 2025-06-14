from fastapi import FastAPI

from src.categories.router import router as categories_router

app = FastAPI()

app.include_router(categories_router, prefix="/api/v1")


@app.get("/ping")
async def pong():
    # await asyncio.sleep(3)
    return {"data": "pong"}
