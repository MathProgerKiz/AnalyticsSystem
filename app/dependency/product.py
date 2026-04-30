from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import async_session_maker
from app.repositories.brand import BrandRepository
from app.repositories.product import ProductRepository
from app.repositories.product_type import ProductTypeRepository
from app.services.brand import BrandService
from app.services.product import ProductService
from app.services.product_type import ProductTypeService


class AppProvider(Provider):

    @provide(scope=Scope.REQUEST)
    async def db(self) -> AsyncIterator[AsyncSession]:
        async with async_session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def product_repository(self, db: AsyncSession) -> ProductRepository:
        return ProductRepository(db)

    @provide(scope=Scope.REQUEST)
    def brand_repository(self, db: AsyncSession) -> BrandRepository:
        return BrandRepository(db)

    @provide(scope=Scope.REQUEST)
    def product_type_repository(self, db: AsyncSession) -> ProductTypeRepository:
        return ProductTypeRepository(db)

    @provide(scope=Scope.REQUEST)
    def product_service(self, repository: ProductRepository) -> ProductService:
        return ProductService(repository)

    @provide(scope=Scope.REQUEST)
    def brand_service(self, repository: BrandRepository) -> BrandService:
        return BrandService(repository)

    @provide(scope=Scope.REQUEST)
    def product_type_service(
        self,
        repository: ProductTypeRepository,
    ) -> ProductTypeService:
        return ProductTypeService(repository)
