from collections.abc import AsyncIterator

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import AsyncSession

from app.analytics.analytics_repositories import AnalyticsRepository
from app.core.database import async_session_maker


class AppProvider(Provider):

    @provide(scope=Scope.REQUEST)
    async def db(self) -> AsyncIterator[AsyncSession]:
        async with async_session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def analytics_repository(self, db: AsyncSession) -> "AnalyticsRepository":
        from app.analytics.analytics_repositories import AnalyticsRepository
        return AnalyticsRepository(db)
