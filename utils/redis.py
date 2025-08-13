from redis.asyncio import Redis
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379')
redis_client = Redis.from_url(REDIS_URL, decode_responses=True)