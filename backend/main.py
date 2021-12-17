from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import feeds, sleep, auth, users, babies, weights, temps, nappies

app = FastAPI(title="Baby Tracker API")

app.include_router(feeds.router)
app.include_router(sleep.router)
app.include_router(users.router)
app.include_router(babies.router)
app.include_router(auth.router)
app.include_router(weights.router)
app.include_router(temps.router)
app.include_router(nappies.router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
