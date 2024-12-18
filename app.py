from fastapi import FastAPI
from config.config import settings
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from helpers.logger import log_info
from router import router
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/")
def root():
    return {"message": "Hello World"}

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_PORT)

