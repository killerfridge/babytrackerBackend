from fastapi import FastAPI
from .routes import feeds, sleep, auth, users

app = FastAPI(title="Baby Tracker API")

app.include_router(feeds.router)
app.include_router(sleep.router)
