from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from models import user_model
from routes import user_route

user_model.Base.metadata.create_all(bind=engine)
app = FastAPI()


@app.get("/apihealthcheck")
async def get_api_status():
    return {"Message": "This API is Live!"}


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_route.router)
