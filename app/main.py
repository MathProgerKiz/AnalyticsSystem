from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from app.api.v1.product import router as product_router
from app.dependency.product import AppProvider

app = FastAPI()
app.include_router(product_router)

container = make_async_container(AppProvider())
setup_dishka(container, app)


@app.get("/")
async def root():
    return {"message": "AI Analytics API is running"}
