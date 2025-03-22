"""
fastapi dev app/main.py --reload
uvicorn app.main:app --reload
uvicorn --host 0.0.0.0 app.main:app
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
fetch('http://localhost:8000/').then(res=>res.json()).then(console.log)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from . import models
from .routers import post, user, auth, vote


# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["https://www.google.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
    

# Request get method url find for the first path match
@app.get("/")
async def root():
    return JSONResponse(content={"message": "Hellu mai Zâu'ss Mezzy xinh đẹp tuỵt zời cụa tui, ci/cd test nè"}, media_type="application/json; charset=utf-8")
# async def root():
#     return {"message": "Hello World"}



