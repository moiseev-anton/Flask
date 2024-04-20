from pydantic import BaseModel, Field, EmailStr


class UserIn(BaseModel):
    firstname: str = Field(..., title='Firstname', max_length=50)
    lastname: str = Field(title='Lastname', max_length=50, default="")
    email: EmailStr = Field(..., title='Email')
    password: str = Field(..., title='Password', min_length=6, max_length=128)


class UserOut(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: EmailStr
