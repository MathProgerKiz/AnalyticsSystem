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
