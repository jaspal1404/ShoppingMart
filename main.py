from fastapi import FastAPI
import models
from database import engine
from routers import shopping

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


app.include_router(shopping.router)