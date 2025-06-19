from fastapi import APIRouter
from fastapi.requests import Request


auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@auth_router.post('/signup')
async def sign_up():
    return ...

@auth_router.get('/signin')
async def login():
    return ...