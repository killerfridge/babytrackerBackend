from fastapi import FastAPI
from .routes import feeds, sleep, auth, users, babies

app = FastAPI(title="Baby Tracker API")

app.include_router(feeds.router)
app.include_router(sleep.router)
app.include_router(users.router)
app.include_router(babies.router)
app.include_router(auth.router)
