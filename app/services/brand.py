class BrandService:
    def __init__(self, brand_repository):
        self.brand_repository = brand_repository

    async def create_brand(self, brand_data):
        return await self.brand_repository.create_brand(brand_data)
