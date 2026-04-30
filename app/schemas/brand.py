from pydantic import BaseModel, ConfigDict, Field


class BrandBase(BaseModel):
    brand_name: str = Field(..., min_length=1, max_length=32)


class BrandCreate(BrandBase):
    pass


class BrandUpdate(BaseModel):
    brand_name: str | None = Field(None, min_length=1, max_length=32)


class BrandDelete(BaseModel):
    id: int


class BrandRead(BrandBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
