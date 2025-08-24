from fastapi import FastAPI
from app.core.database import init_db
from contextlib import asynccontextmanager
from app.routes.docs import router as docs_router
from app.routes.routes import router as routes_router
from app.core.config import TESTING

@asynccontextmanager
async def lifespan(app: FastAPI):
    if TESTING != "1":
        await init_db()
        print("Database created!")
    yield
    
app = FastAPI(lifespan=lifespan)

app.include_router(docs_router)
app.include_router(routes_router)