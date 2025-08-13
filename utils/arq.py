from arq import create_pool
from arq.connections import RedisSettings

# Настройки Redis
REDIS_SETTINGS = RedisSettings(host="localhost", port=6379, database=0)

async def get_redis_pool():
    return await create_pool(REDIS_SETTINGS)