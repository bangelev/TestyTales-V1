from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn

import datetime

from fastapi.middleware.cors import CORSMiddleware

from routes.recipes_routes import recipes_router

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# GET method for root page


@app.get("/", )
async def root():
    return {"recipes": "Maybe later!?"}

app.include_router(recipes_router)

if __name__ == "__main__":
    uvicorn.run("app:app",
                host='0.0.0.0',
                port=4000,
                reload=True,
                log_level="info")
