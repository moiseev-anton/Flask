from fastapi import APIRouter, HTTPException
from typing import List
from homework06.validators import UserIn, UserOut
from homework06.database import database, users
import bcrypt

user_router = APIRouter(tags=["Users"])


@user_router.post("/users/", response_model=UserOut)
async def create_user(user: UserIn):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

    query = users.insert().values(
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
        password=hashed_password
    )

    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}


@user_router.get("/users/", response_model=List[UserOut])
async def read_users():
    query = users.select()
    results = await database.fetch_all(query)
    if not results:
        raise HTTPException(status_code=404, detail="Users not found")
    return results


@user_router.get("/users/{user_id}", response_model=UserOut)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    result = await database.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return result


@user_router.put("/users/{user_id}", response_model=UserOut)
async def update_user(user_id: int, new_user: UserIn):
    hashed_password = bcrypt.hashpw(new_user.password.encode('utf-8'), bcrypt.gensalt())
    new_data = new_user.dict()
    new_data['password'] = hashed_password

    query = (
        users.update()
        .where(users.c.id == user_id)
        .values(**new_data)
    )

    await database.execute(query)
    return {**new_user.dict(), "id": user_id}


@user_router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    result = await database.execute(query)
    if not result:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
