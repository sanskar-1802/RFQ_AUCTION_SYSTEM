from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app import models
from app.routes import rfq, bids, suppliers, logs

app = FastAPI()

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


Base.metadata.create_all(bind=engine)


app.include_router(rfq.router)
app.include_router(bids.router)
app.include_router(suppliers.router)
app.include_router(logs.router)