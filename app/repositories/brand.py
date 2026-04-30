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
