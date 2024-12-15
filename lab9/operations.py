from sqlalchemy.orm import Session
from models import User, Post


def create_user(db: Session, username: str, email: str, password: str):
    db_user = User(username=username, email=email, password=password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_post(db: Session, title: str, content: str, user_id: int):
    db_post = Post(title=title, content=content, user_id=user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def get_users(db: Session):
    return db.query(User).all()

def get_posts(db: Session):
    return db.query(Post).all()

def update_user_email(db: Session, user_id: int, new_email: str):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.email = new_email
        db.commit()
        db.refresh(user)
        return user
    return None

def delete_post(db: Session, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        db.delete(post)
        db.commit()
