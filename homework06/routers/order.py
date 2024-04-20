from fastapi import APIRouter, HTTPException
from typing import List

from homework06.validators import OrderIn, OrderOut
from homework06.database import database, orders, users, products
from datetime import datetime

order_router = APIRouter(tags=["Orders"])


@order_router.post("/orders/", response_model=OrderOut)
async def create_order(order: OrderIn):
    # Проверка на существование пользователя
    user_query = users.select().where(users.c.id == order.user_id)
    user_result = await database.fetch_one(user_query)
    if not user_result:
        raise HTTPException(status_code=404, detail="User not found")

    # Проверка на существование товара
    product_query = products.select().where(products.c.id == order.product_id)
    product_result = await database.fetch_one(product_query)
    if not product_result:
        raise HTTPException(status_code=404, detail="Product not found")

    query = orders.insert().values(
        user_id=order.user_id,
        product_id=order.product_id,
        status=order.status
    )
    last_record_id = await database.execute(query)
    return {**order.dict(), "id": last_record_id, "date": datetime.now()}


@order_router.get("/orders/", response_model=List[OrderOut])
async def get_orders():
    query = orders.select()
    return await database.fetch_all(query)


@order_router.get("/orders/{order_id}/", response_model=OrderOut)
async def get_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    order = await database.fetch_one(query)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@order_router.put("/orders/{order_id}/", response_model=OrderOut)
async def update_order(order_id: int, new_order: OrderIn):
    # Проверка на существование пользователя
    user_query = users.select().where(users.c.id == new_order.user_id)
    user_result = await database.fetch_one(user_query)
    if not user_result:
        raise HTTPException(status_code=404, detail="User not found")

    # Проверка на существование товара
    product_query = products.select().where(products.c.id == new_order.product_id)
    product_result = await database.fetch_one(product_query)
    if not product_result:
        raise HTTPException(status_code=404, detail="Product not found")

    query = (
        orders.update().
        where(orders.c.id == order_id).
        values(
            user_id=new_order.user_id,
            product_id=new_order.product_id,
            status=new_order.status.value
        ).returning(*orders.c)
    )
    order = await database.execute(query)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")

    # мы не изменяем дату создания заказа, но чтобы ее получить делаем еще один запрос к БД
    select_query = orders.select().where(orders.c.id == order_id)
    updated_order = await database.fetch_one(select_query)
    return updated_order


@order_router.delete("/orders/{order_id}/", response_model=dict)
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    result = await database.execute(query)
    if not result:
        raise HTTPException(status_code=404, detail="Order not found")
    return {"message": "Order deleted"}
