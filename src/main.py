from fastapi import FastAPI

app = FastAPI()


@app.get("/ping")
async def pong():
    # await asyncio.sleep(3)
    return {"data": "pong"}
