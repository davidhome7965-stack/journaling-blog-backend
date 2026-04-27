from datetime import datetime
from bson import ObjectId
from app.database.connection import db   # ✅ app. लगा

posts_collection = db.posts

async def get_all_posts() -> list[dict]:
    posts = await posts_collection.find().sort("createdAt", -1).to_list(length=100)
    for post in posts:
        post["_id"] = str(post["_id"])
        post["createdAt"] = post["createdAt"].isoformat() if isinstance(post["createdAt"], datetime) else str(post["createdAt"])
        if "updatedAt" in post and post["updatedAt"]:
            post["updatedAt"] = post["updatedAt"].isoformat() if isinstance(post["updatedAt"], datetime) else str(post["updatedAt"])
    return posts

async def get_post_by_slug(slug: str) -> dict | None:
    post = await posts_collection.find_one({"slug": slug})
    if post:
        post["_id"] = str(post["_id"])
        post["createdAt"] = post["createdAt"].isoformat() if isinstance(post["createdAt"], datetime) else str(post["createdAt"])
        if "updatedAt" in post and post["updatedAt"]:
            post["updatedAt"] = post["updatedAt"].isoformat() if isinstance(post["updatedAt"], datetime) else str(post["updatedAt"])
    return post

async def create_post(data: dict) -> dict:
    post = {
        "title": data["title"],
        "slug": data["slug"],
        "content": data["content"],
        "author": data.get("author", "Admin"),
        "tags": data.get("tags", []),
        "createdAt": datetime.utcnow(),
    }
    result = await posts_collection.insert_one(post)
    post["_id"] = str(result.inserted_id)
    post["createdAt"] = post["createdAt"].isoformat()
    return post

async def update_post(id: str, data: dict) -> dict | None:
    try:
        obj_id = ObjectId(id)
    except:
        return None
    
    update_data = {k: v for k, v in data.items() if v is not None}
    if update_data:
        update_data["updatedAt"] = datetime.utcnow()
    result = await posts_collection.update_one({"_id": obj_id}, {"$set": update_data})
    if result.modified_count:
        return await get_post_by_id(id)
    return None

async def get_post_by_id(id: str) -> dict | None:
    try:
        obj_id = ObjectId(id)
    except:
        return None
    
    post = await posts_collection.find_one({"_id": obj_id})
    if post:
        post["_id"] = str(post["_id"])
        post["createdAt"] = post["createdAt"].isoformat() if isinstance(post["createdAt"], datetime) else str(post["createdAt"])
        if "updatedAt" in post and post["updatedAt"]:
            post["updatedAt"] = post["updatedAt"].isoformat() if isinstance(post["updatedAt"], datetime) else str(post["updatedAt"])
    return post

async def delete_post(id: str) -> bool:
    try:
        obj_id = ObjectId(id)
    except:
        return False
    
    result = await posts_collection.delete_one({"_id": obj_id})
    return result.deleted_count > 0