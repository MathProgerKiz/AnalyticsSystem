

class ProductService:
    def __init__(self, product_repository):
        self.product_repository = product_repository
    
    async def create_product(self, product_data):
        return await self.product_repository.create_product(product_data)
    
    async def get_product(self, product_id):
        return await self.product_repository.get_product(product_id)
    
    async def get_products(self):
        return await self.product_repository.get_products()
    
    async def update_product(self, product_id, product_data):
        return await self.product_repository.update_product(product_id, product_data)

    async def delete_product(self, product_id):
        return await self.product_repository.delete_product(product_id)