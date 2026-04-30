from pydantic import BaseModel, ConfigDict, Field


class ProductTypeBase(BaseModel):
    product_type: str = Field(..., min_length=1, max_length=32)


class ProductTypeCreate(ProductTypeBase):
    pass


class ProductTypeUpdate(BaseModel):
    product_type: str | None = Field(None, min_length=1, max_length=32)


class ProductTypeDelete(BaseModel):
    id: int


class ProductTypeRead(ProductTypeBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


TypeRead = ProductTypeRead
