from sqlalchemy import select

from app.models.product import ProductType


class ProductTypeRepository:
    def __init__(self, db):
        self.db = db

    async def create_product_type(self, product_type_data):
        product_type = ProductType(**product_type_data)
        self.db.add(product_type)
        await self.db.commit()
        await self.db.refresh(product_type)
        return product_type

    async def get_product_type(self, product_type_id):
        query = select(ProductType).where(ProductType.id == product_type_id)
        return await self.db.scalar(query)

    async def get_product_types(self):
        result = await self.db.scalars(select(ProductType))
        return result.all()

    async def update_product_type(self, product_type_id, product_type_data):
        product_type = await self.get_product_type(product_type_id)
        if product_type is None:
            return None
        for key, value in product_type_data.items():
            setattr(product_type, key, value)
        await self.db.commit()
        await self.db.refresh(product_type)
        return product_type

    async def delete_product_type(self, product_type_id):
        product_type = await self.get_product_type(product_type_id)
        if product_type is None:
            return None
        await self.db.delete(product_type)
        await self.db.commit()
        return product_type
