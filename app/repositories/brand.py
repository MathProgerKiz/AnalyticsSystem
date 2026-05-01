from sqlalchemy import select

from app.models.product import BrandFeature


class BrandRepository:
    def __init__(self, db):
        self.db = db

    async def create_brand(self, brand_data):
        brand = BrandFeature(**brand_data)
        self.db.add(brand)
        await self.db.commit()
        await self.db.refresh(brand)
        return brand

    async def get_brand(self, brand_id):
        query = select(BrandFeature).where(BrandFeature.id == brand_id)
        return await self.db.scalar(query)

    async def get_brands(self):
        result = await self.db.scalars(select(BrandFeature))
        return result.all()

    async def update_brand(self, brand_id, brand_data):
        brand = await self.get_brand(brand_id)
        if brand is None:
            return None
        for key, value in brand_data.items():
            setattr(brand, key, value)
        await self.db.commit()
        await self.db.refresh(brand)
        return brand

    async def delete_brand(self, brand_id):
        brand = await self.get_brand(brand_id)
        if brand is None:
            return None
        await self.db.delete(brand)
        await self.db.commit()
        return brand
