from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session_maker
from app.repositories.product import ProductRepository
from app.services.product import ProductService


class AppProvider(Provider):

    @provide(scope=Scope.REQUEST)
    async def db(self) -> AsyncIterator[AsyncSession]:
        async with async_session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def product_repository(self, db: AsyncSession) -> ProductRepository:
        return ProductRepository(db)

    @provide(scope=Scope.REQUEST)
    def product_service(self, repository: ProductRepository) -> ProductService:
        return ProductService(repository)
