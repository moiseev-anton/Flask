from fastapi import FastAPI
from routers import user_router, product_router, order_router
from database import database
import uvicorn

app = FastAPI()


async def startup_event():
    await database.connect()


async def shutdown_event():
    await database.disconnect()


app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)

app.include_router(user_router)
app.include_router(product_router)
app.include_router(order_router)

if __name__ == '__main__':
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
