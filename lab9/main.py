from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models import init_db, SessionLocal
import operations

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()


@app.on_event("startup")
def startup():
    init_db()


@app.post("/users/")
def create_user(username: str, email: str, password: str, db: Session = Depends(get_db)):
    return operations.create_user(db=db, username=username, email=email, password=password)


@app.post("/posts/")
def create_post(title: str, content: str, user_id: int, db: Session = Depends(get_db)):
    return operations.create_post(db=db, title=title, content=content, user_id=user_id)


@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    return operations.get_users(db=db)


@app.get("/posts/")
def get_posts(db: Session = Depends(get_db)):
    return operations.get_posts(db=db)


@app.patch("/users/{user_id}/")
def update_user_email(user_id: int, new_email: str, db: Session = Depends(get_db)):
    user = operations.update_user_email(db=db, user_id=user_id, new_email=new_email)
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


@app.delete("/posts/{post_id}/")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    operations.delete_post(db=db, post_id=post_id)
    return {"message": "Пост удален успешно"}
