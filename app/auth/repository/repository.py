from datetime import datetime
from fastapi import HTTPException
from bson.objectid import ObjectId
from pymongo.database import Database

from ..utils.security import hash_password


class AuthRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_user(self, user: dict):
        payload = {
            "email": user["email"],
            "password": hash_password(user["password"]),
            "phone": user["phone"],
            "name": user["name"],
            "city": user["city"],
            "created_at": datetime.utcnow(),
        }

        self.database["users"].insert_one(payload)

    def get_user_by_id(self, user_id: str) -> dict | None:
        user = self.database["users"].find_one(
            {
                "_id": ObjectId(user_id),
            }
        )
        return user

    def get_user_by_email(self, email: str) -> dict | None:
        user = self.database["users"].find_one(
            {
                "email": email,
            }
        )
        return user

    def update_user(self, user_id: str, data: dict):
        self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={
                "$set": {
                    "phone": data["phone"],
                    "name": data["name"],
                    "city": data["city"],
                }
            },
        )

    def add_to_favorite(self, id: str, user_id: str):
        shanyrak = self.database["shanyraks"].find_one({"_id": ObjectId(id)})
        if shanyrak == None:
            raise HTTPException(status_code=404, detail="There is no such shanyrak:(")
        payload = {"_id": ObjectId(id), "address": shanyrak["address"]}
        self.database["users"].update_one(
            {"_id": ObjectId(user_id)}, {"$push": {"shanyraks": payload}}
        )

    def get_favorites(self, user_id: str):
        user = self.database["users"].find_one({"_id": ObjectId(user_id)})
        if user["shanyraks"] == None:
            raise HTTPException(status_code=404, detail="You have no favorites!")
        return user["shanyraks"]

    def delete_from_favorites(self, id: str, user_id: str):
        user = self.database["users"].find_one({"_id": ObjectId(user_id)})
        favorites = user["shanyraks"]
        delete_item = {}
        for favorite in favorites:
            if favorite["_id"] == ObjectId(id):
                delete_item = favorite
        if delete_item != {}:
            favorites.remove(delete_item)
        self.database["users"].update_one(
            {"_id": ObjectId(user_id)}, {"$set": {"shanyraks": favorites}}
        )

    def upload_avatar(self, user_id: str, url: str):
        self.database["users"].update_one(
            filter={"_id": ObjectId(user_id)},
            update={"$set": {"avatar_url": url}},
        )

    def delete_avatar(self, user_id: str):
        self.database["users"].update_one(
            {"_id": ObjectId(user_id)}, {"$set": {"avatar_url": ""}}
        )
