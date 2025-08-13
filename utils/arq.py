from arq import create_pool
from arq.connections import RedisSettings
import os

# Настройки Redis
REDIS_URL = os.getenv('REDIS_URL', 'redis://redis:6379')
REDIS_SETTINGS = RedisSettings.from_dsn(REDIS_URL)

async def get_redis_pool():
    return await create_pool(REDIS_SETTINGS)