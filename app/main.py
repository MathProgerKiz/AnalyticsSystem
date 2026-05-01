from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from app.api.v1.analytics import router as analytics_router
from app.api.v1.brand import router as brand_router
from app.api.v1.product import router as product_router
from app.api.v1.product_type import router as product_type_router
from app.dependency.product import AppProvider

app = FastAPI()
app.include_router(brand_router)
app.include_router(product_router)
app.include_router(product_type_router)
app.include_router(analytics_router)

container = make_async_container(AppProvider())
setup_dishka(container, app)


@app.get("/")
async def root():
    return {"message": "AI Analytics API is running"}
