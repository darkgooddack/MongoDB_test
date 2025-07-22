from typing import Optional, List
from bson import ObjectId
from app.models.user import User, UserCreate
from app.core.db import db


class UserRepository:

    collection = db.users

    async def create(self, obj: UserCreate) -> User:
        obj_dict = obj.model_dump(by_alias=True)
        result = await self.collection.insert_one(obj_dict)
        return User(id=str(result.inserted_id), **obj_dict)

    async def get(self, id: str) -> Optional[User]:
        data = await self.collection.find_one({"_id": ObjectId(id)})
        if data:
            data["id"] = str(data["_id"])
            data.pop("_id")
            return User(**data)
        return None

    async def list(self) -> List[User]:
        cursor = self.collection.find()
        users = []
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            doc.pop("_id")
            users.append(User(**doc))
        return users

    async def update(self, id: str, obj: UserCreate) -> Optional[User]:
        obj_dict = obj.model_dump()
        result = await self.collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": obj_dict}
        )
        if result.modified_count == 1:
            return await self.get(id)
        return None

    async def delete(self, id: str) -> bool:
        result = await self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count == 1
