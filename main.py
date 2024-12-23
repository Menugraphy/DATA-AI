from fastapi import FastAPI
import uvicorn
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from loguru import logger

from router.menu_route import menu_router, get_connect_s3, get_connect_db

from starlette.middleware.cors import CORSMiddleware

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    get_connect_s3()
    logger.info("S3 connected")
    get_connect_db()
    logger.info("DB connected")
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(menu_router, prefix="/menu")

# CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8080)
