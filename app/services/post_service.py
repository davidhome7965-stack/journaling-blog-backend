from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.post import Post
from app.database.postgres import AsyncSessionLocal
from datetime import datetime

async def get_all_posts():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Post).order_by(Post.created_at.desc()))
        posts = result.scalars().all()
        return [p.to_dict() for p in posts]

async def get_post_by_slug(slug: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Post).where(Post.slug == slug))
        post = result.scalar_one_or_none()
        return post.to_dict() if post else None

async def get_post_by_id(post_id: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Post).where(Post.id == post_id))
        post = result.scalar_one_or_none()
        return post.to_dict() if post else None

async def create_post(data: dict):
    async with AsyncSessionLocal() as session:
        new_post = Post(
            title=data["title"],
            slug=data["slug"],
            content=data["content"],
            author=data.get("author", "Admin"),
            tags=data.get("tags", []),
        )
        session.add(new_post)
        await session.commit()
        await session.refresh(new_post)
        return new_post.to_dict()

async def update_post(post_id: str, data: dict):
    async with AsyncSessionLocal() as session:
        stmt = update(Post).where(Post.id == post_id).values(**data, updated_at=datetime.utcnow())
        await session.execute(stmt)
        await session.commit()
        return await get_post_by_id(post_id)

async def delete_post(post_id: str) -> bool:
    async with AsyncSessionLocal() as session:
        stmt = delete(Post).where(Post.id == post_id)
        result = await session.execute(stmt)
        await session.commit()
        return result.rowcount > 0