from datetime import datetime

from fastapi import HTTPException

from bson.objectid import ObjectId
from pymongo.database import Database

from ..utils.security import hash_password


class ShanyraqsRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_shanyraq(self, user_id: str, shanyraq: dict):
        payload = {
            "type": shanyraq["type"],
            "price": shanyraq["price"],
            "address": shanyraq["address"],
            "area": shanyraq["area"],
            "rooms_count": shanyraq["rooms_count"],
            "description": shanyraq["description"],
            "created_at": datetime.utcnow(),
            "user_id": ObjectId(user_id),
        }
        new_shanyraq = self.database["shanyraqs"].insert_one(payload)
        return new_shanyraq.inserted_id

    def get_shanyraq_by_id(self, id: str):
        shanyraq = self.database["shanyraqs"].find_one({"_id": ObjectId(id)})
        if shanyraq:
            return shanyraq
        else:
            raise HTTPException(status_code=404, detail="There is no such shanyraq:()")

    def update_shanyraq(self, id: str, user_id: str, input: dict):
        check_exist = self.database["shanyraqs"].find_one(
            {"$and": [{"_id": ObjectId(id)}, {"user_id": ObjectId(user_id)}]}
        )
        if check_exist:
            response = self.database["shanyraqs"].update_one(
                {"$and": [{"_id": ObjectId(id)}, {"user_id": ObjectId(user_id)}]},
                {
                    "$set": {
                        "type": input["type"],
                        "price": input["price"],
                        "address": input["address"],
                        "area": input["area"],
                        "rooms_count": input["rooms_count"],
                        "description": input["description"],
                    }
                },
            )
        else:
            raise HTTPException(status_code=404, detail="There is no sych shanyraq:(")

        return response

    def delete_shanyraq(self, id: str, user_id: str):
        check_exist = self.database["shanyraqs"].find_one(
            {"$and": [{"_id": ObjectId(id)}, {"user_id": ObjectId(user_id)}]}
        )
        if check_exist:
            self.database["shanyraqs"].delete_one({"_id": ObjectId(id)})
        else:
            raise HTTPException(status_code=404, detail="No permission>:()")
