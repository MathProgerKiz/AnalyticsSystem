class ProductTypeService:
    def __init__(self, product_type_repository):
        self.product_type_repository = product_type_repository

    async def create_product_type(self, product_type_data):
        return await self.product_type_repository.create_product_type(product_type_data)
