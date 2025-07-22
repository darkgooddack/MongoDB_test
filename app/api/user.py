from fastapi import APIRouter, HTTPException
from app.repositories.user_repository import UserRepository
from app.models.user import User, UserCreate

router = APIRouter()
user_repo = UserRepository()


@router.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    return await user_repo.create(user)


@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: str):
    user = await user_repo.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


@router.get("/users/", response_model=list[User])
async def all_users():
    users = await user_repo.list()
    if not users:
        raise HTTPException(status_code=404, detail="Список пользователей пуст")
    return users


@router.put("/users/{user_id}", response_model=User)
async def update_user(user_id: str, obj: UserCreate):
    user = await user_repo.update(user_id, obj)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


@router.delete("/users/{user_id}")
async def delete_user(user_id: str):
    success = await user_repo.delete(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Не удалось удалить пользователя")
    return {"deleted": success}
