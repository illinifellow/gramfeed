release: cd backend && alembic upgrade head
web: cd backend && uvicorn gramfeed.api.app:app --host 0.0.0.0 --port $PORT
worker: cd backend && rq worker fetch --url $GRAMFEED_REDIS_URL
clock: cd backend && python -m gramfeed.clock
