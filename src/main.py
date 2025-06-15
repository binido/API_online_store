from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from src.auth.router import router as auth_router
from src.categories.router import router as categories_router
from src.orders.router import router as orders_router
from src.products.router import router as products_router
from src.users.router import router as users_router

app = FastAPI(
    title="API",
    swagger_ui_parameters={"persistAuthorization": True},
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Интернет-магазин API",
        version="1.0.0",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "HTTPBearer": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Введите JWT токен, полученный при логине",
        }
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

app.include_router(users_router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1")
app.include_router(categories_router, prefix="/api/v1")
app.include_router(products_router, prefix="/api/v1")
app.include_router(orders_router, prefix="/api/v1")


@app.get("/ping")
async def pong():
    # await asyncio.sleep(3)
    return {"data": "pong"}
