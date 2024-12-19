from app import db
from sqlalchemy import Column, Integer, String, Text
from database import Base

class BookPost(Base):
    __tablename__ = 'book_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    book_condition = db.Column(db.Text, nullable=True)
    price = db.Column(db.Integer, nullable=False)
    post_time = db.Column(db.DATETIME , nullable=False)
    seller_id = db.Column(db.INTEGER, nullable=False)