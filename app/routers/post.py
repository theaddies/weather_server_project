from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter, Header
from .. import models, schemas, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import Date, cast
from ..database import engine, get_db
from datetime import date, timedelta, datetime, timezone

from typing import List, Optional

from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
#    posts.headers.add('Access-Control-Allow-Origin', '*')
    return posts

@router.get("/day")#, response_model=schemas.Post)
def get_post( db: Session = Depends(get_db)):
    now = datetime.now(timezone(timedelta(hours=-4), 'EST'))
    print(now)
    twenty_four_hours_ago = now - timedelta(hours=24)
    print(twenty_four_hours_ago)
    post = db.query(models.Post).filter(models.Post.created_at.between(twenty_four_hours_ago, now)).all()
   # post = db.query(models.Post).filter((cast(models.Post.created_at,Date)) > twenty_four_hours_ago).all()
    #printing post above without the .first() shows teh query
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail =f"Last post not found" )
    return post

@router.get("/hour")#, response_model=schemas.Post)
def get_post( db: Session = Depends(get_db)):
    now = datetime.now(timezone(timedelta(hours=-4), 'EST'))
    print(now)
    one_hour_ago = now - timedelta(hours=1)
    print(one_hour_ago)
    post = db.query(models.Post).filter(models.Post.created_at.between(one_hour_ago, now)).all()
   # post = db.query(models.Post).filter((cast(models.Post.created_at,Date)) > twenty_four_hours_ago).all()
    #printing post above without the .first() shows teh query
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail =f"Last post not found" )
    return post

@router.get("/date/{start_date}/{end_date}")#, response_model=schemas.Post)
def get_post(start_date: str, end_date: str, db: Session = Depends(get_db)):
    #now = datetime.now(timezone(timedelta(hours=-4), 'EST'))
    end_date_dt = datetime.strptime(end_date, "%Y-%m-%d")
    #print(end_date_dt)
    #print('date =', date)
    start_date_dt = datetime.strptime(start_date, "%Y-%m-%d")
    #print(start_date_dt)
    post = db.query(models.Post).filter(models.Post.created_at.between(start_date_dt, end_date_dt)).all()
   # post = db.query(models.Post).filter((cast(models.Post.created_at,Date)) > twenty_four_hours_ago).all()
    #printing post above without the .first() shows teh query
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail =f"Last post not found" )
    return post

@router.get("/last", response_model=schemas.Post)
def get_post(db: Session = Depends(get_db)):
    post = db.query(models.Post).order_by(models.Post.id.desc()).first()
    #printing post above without the .first() shows teh query
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail =f"Last post not found" )
    return post

@router.get("/first", response_model=schemas.Post)
def get_post(db: Session = Depends(get_db)):
    post = db.query(models.Post).order_by(models.Post.id.asc()).first()
    #printing post above without the .first() shows teh query
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail =f"Last post not found" )
    return post

@router.get("/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM weather_data WHERE id = %s""", (str(id)))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    #printing post above without the .first() shows teh query
    #print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail =f"post with id: {id} was not found" )
    return post



#this is getting a post with old sql
# @app.get("/posts")
# async def get_posts():
#     cursor.execute("""SELECT * FROM weather_data """)
#     posts = cursor.fetchall()
#     return{"data": posts}

#the old way to make a post
# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_posts(post: Post):
#     print('*************************************************')
#     print(post.temp)
#     cursor.execute("""INSERT INTO weather_data (temp, press, humid, wind_speed, wind_direction, event_direction,
#     bno_direction, current, voltage, power, date) VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s, %s, %s) RETURNING * """,
#     (post.temp, post.press, post.humid, post.wind_speed, post.wind_direction, post.bno_direction, post.event_direction, post.current,
#     post.voltage, post.power, post.date))
#     # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) RETURNING *""",
#     # (post.title, post.content, post.published))
#     new_post = cursor.fetchone()
#     conn.commit()
#     return{"data": new_post}

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
#def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    #the line above does all of this
    # new_post = models.Post(temp = post.temp, press = post.press, humid = post.humid, wind_speed = post.wind_speed,
    # wind_direction = post.wind_direction, event_direction = post.event_direction, bno_direction = post.bno_direction,
    # current = post.current, voltage = post.voltage, power = post.power, date = post.date)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM weather_data WHERE id = %s RETURNING *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
        detail = f"post with id: {id} does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code =status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE weather_data SET temp = %s, press = %s, humid = %s, wind_speed = %s, wind_direction = %s,
    # event_direction = %s, bno_direction = %s, current = %s, voltage = %s, power = %s, date = %s WHERE id = %sRETURNING * """, 
    # (post.temp, post.press, post.humid, post.wind_speed, post.wind_direction, post.bno_direction, post.event_direction, post.current,
    # post.voltage, post.power, post.date, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
   #print(post_query)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
        detail = f"post with id: {id} does not exist")

    #print(updated_post.dict())
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()