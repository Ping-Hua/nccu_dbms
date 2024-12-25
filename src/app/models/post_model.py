from app import db
from sqlalchemy import Column, Integer, String, Text
from database import Base
'''
class BookPost(Base):
    __tablename__ = 'book_posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    book_condition = db.Column(db.Text, nullable=True)
    price = db.Column(db.Integer, nullable=False)
    post_time = db.Column(db.DATETIME , nullable=False)
    seller_id = db.Column(db.INTEGER, nullable=False)
'''

class Post(db.Model):
    __tablename__ = 'posts'

    post_id = db.Column(db.Integer, primary_key=True)
    # seller_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    seller_user_id = db.Column(db.Integer, nullable=False)
    # book_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, nullable=False)
    book_condition = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    create_time = db.Column(db.DateTime, default=db.func.current_timestamp())

    def to_dict(self):
        return {
            "post_id": self.post_id,
            "seller_user_id": self.seller_user_id,
            "book_id": self.book_id,
            "book_condition": self.book_condition,
            "price": self.price,
            "create_time": self.create_time.isoformat() if self.create_time else None 
        }