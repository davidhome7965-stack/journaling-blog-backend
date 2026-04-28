from fastapi import APIRouter, HTTPException, Depends, Request
from app.schemas.post import PostCreate, PostUpdate, PostResponse
import app.services.post_service as post_service
from app.routes.auth import verify_token
# ... the rest of your route code unchanged ... 

router = APIRouter(prefix="/posts", tags=["posts"])

async def check_auth(request: Request):
    auth = request.headers.get("Authorization", "")
    token = auth.replace("Bearer ", "") if auth.startswith("Bearer ") else ""
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True

@router.get("", response_model=list[PostResponse])
async def get_all_posts():
    posts = await post_service.get_all_posts()
    return posts

@router.get("/{slug}", response_model=PostResponse)
async def get_post(slug: str):
    post = await post_service.get_post_by_slug(slug)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.post("", response_model=PostResponse)
async def create_post(data: PostCreate, auth: bool = Depends(check_auth)):
    existing = await post_service.get_post_by_slug(data.slug)
    if existing:
        raise HTTPException(status_code=400, detail="Slug already exists")
    post = await post_service.create_post(data.model_dump())
    return post

@router.put("/{id}", response_model=PostResponse)
async def update_post(id: str, data: PostUpdate, auth: bool = Depends(check_auth)):
    post = await post_service.update_post(id, data.model_dump(exclude_none=True))
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.delete("/{id}")
async def delete_post(id: str, auth: bool = Depends(check_auth)):
    deleted = await post_service.delete_post(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Post not found")
    return {"message": "Post deleted successfully"}