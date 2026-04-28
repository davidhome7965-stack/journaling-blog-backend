from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "journaling_blog")

# SSL/TLS विकल्पों के साथ क्लाइंट बनाएँ
client = AsyncIOMotorClient(
    MONGO_URI,
    tlsAllowInvalidCertificates=True,   # अस्थायी समाधान – SSL सत्यापन बंद
    tlsAllowInvalidHostnames=True,      # होस्टनेम मिलान बंद
)

db = client[DB_NAME]

async def ping_db():
    await client.admin.command('ping')
    print("✅ Database connected successfully")
