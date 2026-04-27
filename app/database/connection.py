from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

# .env फ़ाइल से वेरिएबल्स लोड करें
load_dotenv()

# MongoDB का connection string (URI) .env से लें, या डिफ़ॉल्ट localhost use करें
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

# MongoDB क्लाइंट बनाएँ (async)
client = AsyncIOMotorClient(MONGO_URI)

# डेटाबेस का नाम चुनें (जैसे "journaling_blog")
DB_NAME = os.getenv("DB_NAME", "journaling_blog")
db = client[DB_NAME]

# (Optional) एक बार डेटाबेस कनेक्शन चेक करने के लिए फंक्शन
async def ping_db():
    """Check if database is reachable"""
    await client.admin.command('ping')
    print("✅ Database connected successfully")