class BrandService:
    def __init__(self, brand_repository):
        self.brand_repository = brand_repository

    async def create_brand(self, brand_data):
        return await self.brand_repository.create_brand(brand_data)

    async def get_brand(self, brand_id):
        return await self.brand_repository.get_brand(brand_id)

    async def get_brands(self):
        return await self.brand_repository.get_brands()

    async def update_brand(self, brand_id, brand_data):
        return await self.brand_repository.update_brand(brand_id, brand_data)

    async def delete_brand(self, brand_id):
        return await self.brand_repository.delete_brand(brand_id)
