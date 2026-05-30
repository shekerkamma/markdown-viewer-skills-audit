from arq.connections import RedisSettings

from app.config import settings
from app.tasks.pipeline import run_pipeline


def parse_redis_url(url: str) -> RedisSettings:
    from urllib.parse import urlparse

    parsed = urlparse(url)
    return RedisSettings(
        host=parsed.hostname or "localhost",
        port=parsed.port or 6379,
        database=int(parsed.path.lstrip("/") or 0),
        password=parsed.password,
    )


class WorkerSettings:
    functions = [run_pipeline]
    redis_settings = parse_redis_url(settings.redis_url)
