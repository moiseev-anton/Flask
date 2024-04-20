from pydantic import BaseModel, Field


class ProductIn(BaseModel):
    title: str = Field(..., title='Title', max_length=100)
    description: str = Field(None, title='Description')
    price: float = Field(..., title='Price', gt=0)


class ProductOut(BaseModel):
    id: int
    title: str
    description: str
    price: float
