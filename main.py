from fastapi import FastAPI, Query, Header, Request, status
from fastapi.exceptions import (
    RequestValidationError,
    HTTPException,
    StarletteHTTPException,
)
from enum import Enum
from pydantic import BaseModel, ConfigDict
from typing import Annotated
from fastapi.responses import JSONResponse

app = FastAPI()


@app.exception_handler(StarletteHTTPException)
@app.exception_handler(RequestValidationError)
async def handle_http_exception(request: Request, exc: Exception):
    return JSONResponse(
        status_code=200,
        content={
            "data": {},
            "code": 0,
        },
    )


class Gender(str, Enum):
    male = "Male"
    female = "Female"


class User(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    age: int


class Header_Data(BaseModel):
    model_config = ConfigDict(extra="allow")
    user_agent: str | None = None
    accept_language: str | None = None


@app.get("/home/{user_id}")
async def root(user_id: int):

    return {"message": f"Welcome to the home page of user {user_id}"}


@app.get("/sex/{gender}")
async def get_gender(gender: Gender):
    return {"message": f"Your gender is {gender.value}"}


@app.get("/items")
async def get_items(page: int = 1, size: int = 10):
    print(f"Retrieving items for page {page} with size {size}")
    return {"items": ["item1", "item2", "item3"]}


@app.post("/get_users")
async def get_users(user: User):
    return user


@app.get("/search")
async def search(
    q: Annotated[
        str | None,
        Query(description="The search query", alias="query", max_length=3),
    ] = None,
):
    if q:
        return {"message": f"Searching for {q}"}
    else:
        return {"message": "No search query provided"}


@app.get("/detail/{detail_id}")
async def get_detail(
    detail_id: int,
    page: Annotated[int, Query(description="The page number", alias="q")] = 1,
    size: int = 10,
):
    if detail_id < 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Detail ID must be a positive integer",
        )

    return {
        "message": f"Detail ID 1111 is {detail_id} and page is {page} with size {size}"
    }


@app.post("/create_user")
async def create_user(
    user: User,
    header: Annotated[Header_Data, Header(description="The header information")] = None,
    request: Request = None,
):
    print(user.model_dump_json())
    print(user.model_extra)
    print(header.model_dump())
    print(request.headers)
    return {"message": f"User {user.name} created successfully with age {user.age}"}
