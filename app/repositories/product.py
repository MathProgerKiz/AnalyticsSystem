

from app.models.product import Product


class ProductRepositiries:
    def __init__(self,db):
        self.db = db 
    
    async def create_product(self, product_data):
        product = Product(**product_data)
        self.db.add(product)
        await self.db.commit()
        await self.db.refresh(product)
        return product
    
    async def get_product(self, product_id):
        return await self.db.get(Product, product_id)
    
    async def update_product(self, product_id, product_data):
        product = await self.get_product(product_id)
        for key, value in product_data.items():
            setattr(product, key, value)
        await self.db.commit()
        await self.db.refresh(product)
        return product
    
    async def delete_product(self, product_id):
        product = await self.get_product(product_id)
        await self.db.delete(product)
        await self.db.commit()  