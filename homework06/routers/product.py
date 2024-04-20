from fastapi import APIRouter, HTTPException
from typing import List
from homework06.validators import ProductIn, ProductOut
from homework06.database import database, products

product_router = APIRouter(tags=["Products"])


@product_router.post("/products/", response_model=ProductOut)
async def create_product(product: ProductIn):
    query = products.insert().values(
        title=product.title,
        description=product.description,
        price=product.price,
    )
    last_record_id = await database.execute(query)
    return {**product.dict(), "id": last_record_id}


@product_router.get("/products/", response_model=List[ProductOut])
async def read_products():
    query = products.select()
    results = await database.fetch_all(query)
    if not results:
        raise HTTPException(status_code=404, detail="Products not found")
    return results


@product_router.get("/products/{product_id}", response_model=ProductOut)
async def read_product(product_id: int):
    query = products.select().where(products.c.id == product_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Product not found")
    return result


@product_router.put("/products/{product_id}", response_model=ProductOut)
async def update_product(product_id: int, new_product: ProductIn):
    query = (
        products.update()
        .where(products.c.id == product_id)
        .values(**new_product.dict())
    )
    await database.execute(query)
    return {**new_product.dict(), "id": product_id}


@product_router.delete("/products/{product_id}")
async def delete_product(product_id: int):
    query = products.delete().where(products.c.id == product_id)
    result = await database.execute(query)
    if not result:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted"}
