

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.models.product import Product


class ProductRepository:
    def __init__(self,db):
        self.db = db 
    
    async def create_product(self, product_data):
        product = Product(**product_data)
        self.db.add(product)
        await self.db.commit()
        return await self.get_product(product.id)
    
    async def get_product(self, product_id):
        query = (
            select(Product)
            .where(Product.id == product_id)
            .options(
                selectinload(Product.brand),
                selectinload(Product.product_type),
            )
        )
        return await self.db.scalar(query)
    
    async def get_products(self):
        query = select(Product).options(
            selectinload(Product.brand),
            selectinload(Product.product_type),
        )
        result = await self.db.scalars(query)
        return result.all()
    
    async def update_product(self, product_id, product_data):
        product = await self.get_product(product_id)
        if product is None:
            return None
        for key, value in product_data.items():
            setattr(product, key, value)
        await self.db.commit()
        return await self.get_product(product.id)
    
    async def delete_product(self, product_id):
        product = await self.get_product(product_id)
        if product is None:
            return None
        await self.db.delete(product)
        await self.db.commit()
        return product
