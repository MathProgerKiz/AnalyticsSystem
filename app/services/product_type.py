class ProductTypeService:
    def __init__(self, product_type_repository):
        self.product_type_repository = product_type_repository

    async def create_product_type(self, product_type_data):
        return await self.product_type_repository.create_product_type(product_type_data)

    async def get_product_type(self, product_type_id):
        return await self.product_type_repository.get_product_type(product_type_id)

    async def get_product_types(self):
        return await self.product_type_repository.get_product_types()

    async def update_product_type(self, product_type_id, product_type_data):
        return await self.product_type_repository.update_product_type(
            product_type_id,
            product_type_data,
        )

    async def delete_product_type(self, product_type_id):
        return await self.product_type_repository.delete_product_type(product_type_id)
