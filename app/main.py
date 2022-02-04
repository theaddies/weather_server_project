from click import DateTime
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
import numpy as np
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import models, schemas
from sqlalchemy.orm import Session
from .database import engine, get_db
from .routers import post, user, auth
from .config import settings

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database='weather_server', user = 'postgres',
        password = 'Lilly911a', cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print('database connection made')
        break
    except Exception as error:
        print('connecting to database failed.')
        print('the error was', error)
        time.sleep(2)

# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p

# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i



@app.get("/")
def root():
    return{"message": "hello world"}