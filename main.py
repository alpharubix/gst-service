from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.database import connect_db, close_db
import uvicorn
from src.config import settings
from src.routes.gst_service import router as gst_router 

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()   # runs when server STARTS
    yield
    await close_db()     # runs when server STOPS

app = FastAPI(lifespan=lifespan)
app.include_router(gst_router)

@app.get("/")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=True)