from datetime import datetime
import random
from fastapi import HTTPException

from bson.objectid import ObjectId
from pymongo.database import Database


class ShanyraksRepository:
    def __init__(self, database: Database):
        self.database = database

    def create_shanyrak(self, user_id: str, shanyrak: dict, coordinates: dict):
        payload = {
            "type": shanyrak["type"],
            "price": shanyrak["price"],
            "address": shanyrak["address"],
            "area": shanyrak["area"],
            "rooms_count": shanyrak["rooms_count"],
            "description": shanyrak["description"],
            "location": [coordinates["lng"], coordinates["lat"]],
            "created_at": datetime.utcnow(),
            "user_id": ObjectId(user_id),
        }
        new_shanyrak = self.database["shanyraks"].insert_one(payload)
        return new_shanyrak.inserted_id

    def get_shanyrak_by_id(self, id: str):
        if len(id) < 24:
            return
        shanyrak = self.database["shanyraks"].find_one({"_id": ObjectId(id)})
        if shanyrak:
            return shanyrak

    def update_shanyrak(self, id: str, user_id: str, input: dict):
        check_exist = self.database["shanyraks"].find_one(
            {"$and": [{"_id": ObjectId(id)}, {"user_id": ObjectId(user_id)}]}
        )
        if check_exist:
            response = self.database["shanyraks"].update_one(
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
            raise HTTPException(status_code=404, detail="There is no sych shanyrak:(")

        return response

    def delete_shanyrak(self, id: str, user_id: str):
        check_exist = self.database["shanyraks"].find_one(
            {"$and": [{"_id": ObjectId(id)}, {"user_id": ObjectId(user_id)}]}
        )
        if check_exist:
            self.database["shanyraks"].delete_one({"_id": ObjectId(id)})
        else:
            raise HTTPException(status_code=404, detail="No permission>:()")

    def post_comment(self, id: str, user_id: str, input: dict):
        payload = {
            "id": str(id) + str(random.randint(1, 10000)),
            "content": input["content"],
            "created_at": datetime.utcnow(),
            "author_id": ObjectId(user_id),
        }
        shanyrak = self.database["shanyraks"].find_one({"_id": ObjectId(id)})
        if shanyrak == None:
            raise HTTPException(status_code=404, detail="There is no such shanyrak:(")
        new_comment = self.database["shanyraks"].update_one(
            {"_id": ObjectId(id)}, {"$push": {"comments": payload}}
        )
        return new_comment

    def get_comments(self, id: str):
        shanyrak = self.database["shanyraks"].find_one({"_id": ObjectId(id)})
        return shanyrak.get("comments")

    def update_comment(self, id: str, comment_id: str, user_id: str, input: dict):
        shanyrak = self.database["shanyraks"].find_one({"_id": ObjectId(id)})
        if shanyrak == None:
            raise HTTPException(status_code=404, detail="There is no such shanyrak:(")

        shanyrak_comments = shanyrak.get("comments")
        for comment in shanyrak_comments:
            if comment.get("id") == comment_id:
                if str(comment.get("author_id")) != str(user_id):
                    raise HTTPException(
                        status_code=403, detail="You can't change someone's comment!"
                    )
                self.database["shanyraks"].update_one(
                    {"$and": [{"_id": ObjectId(id)}, {"comments.id": comment_id}]},
                    {"$set": {"comments.$.content": input["content"]}},
                )
                return input["content"]
        raise HTTPException(status_code=404, detail="There is no such comment:(")

    def delete_comment(self, id: str, comment_id: str, user_id: str):
        shanyrak = self.database["shanyraks"].find_one({"_id": ObjectId(id)})
        if shanyrak == None:
            raise HTTPException(status_code=404, detail="There is no such shanyrak:(")

        shanyrak_comments = shanyrak.get("comments")
        delete_index = -1
        for i, comment in enumerate(shanyrak_comments):
            if comment.get("id") == comment_id:
                if str(comment.get("author_id")) != str(user_id):
                    raise HTTPException(
                        status_code=403, detail="You can't change someone's comment!"
                    )
                delete_index = i

        if delete_index != -1:
            shanyrak_comments.pop(delete_index)
            self.database["shanyraks"].update_one(
                {"$and": [{"_id": ObjectId(id)}, {"comments.id": comment_id}]},
                {"$set": {"comments": shanyrak_comments}},
            )
            return
        raise HTTPException(status_code=404, detail="There is no such comment:(")

    def add_media(self, id: str, user_id: str, urls: list):
        shanyrak = self.database["shanyraks"].find_one({"_id": ObjectId(id)})
        if shanyrak == None:
            raise HTTPException(status_code=404, detail="There is no such shanyrak:(")
        if str(shanyrak.get("user_id")) != str(user_id):
            raise HTTPException(
                status_code=403, detail="You can't add media to this shanyrak!"
            )
        for url in urls:
            self.database["shanyraks"].update_one(
                {"_id": ObjectId(id)}, {"$push": {"media": str(url)}}
            )

    def delete_media(self, id: str, user_id: str, input: dict):
        shanyrak = self.database["shanyraks"].find_one({"_id": ObjectId(id)})
        if shanyrak == None:
            raise HTTPException(status_code=404, detail="There is no such shanyrak:(")
        if str(shanyrak.get("user_id")) != str(user_id):
            raise HTTPException(
                status_code=403, detail="You can't delete media from this shanyrak!"
            )
        new_media = shanyrak["media"]
        for element in input["media"]:
            new_media.remove(element)
        self.database["shanyraks"].update_one(
            {"_id": ObjectId(id)},
            {"$set": {"media": new_media}},
        )

    def find_shanyraks(
        self,
        limit: int,
        offset: int,
        type_of: str,
        rooms_count: int,
        price_from: int,
        price_until: int,
        latitude: float,
        longitude: float,
        radius: float,
    ):
        self.database["shanyraks"].create_index([("location", "2dsphere")])

        location_query = {
            "location": {
                "$near": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": [longitude, latitude],
                    },
                    "$maxDistance": radius,
                }
            }
        }

        def prepare(item):
            item["_id"] = str(item["_id"])
            item.pop("created_at")
            item.pop("user_id")
            if "comments" in item:
                item.pop("comments")
            return item

        filters = [{}]
        if type_of != "":
            filters.append({"type": type_of})
        if rooms_count != 0:
            filters.append({"rooms_count": rooms_count})
        if price_from != 0:
            filters.append({"price": {"$gt": price_from}})
        if price_until != 0:
            filters.append({"price": {"$lt": price_until}})

        if latitude != None or longitude != None or radius != None:
            if (latitude != None and longitude != None and radius != None) == False:
                raise HTTPException(
                    status_code=400,
                    detail="All 3 fields (lng, lat, rad) should be filled",
                )
            filters.append(location_query)

        result = []
        objects = (
            self.database["shanyraks"].find({"$and": filters}).limit(limit).skip(offset)
        )
        total = self.database["shanyraks"].count_documents({"$and": filters})

        for item in objects:
            result.append(item)
        result = list(map(prepare, result))
        return {"total": total, "objects": result}
