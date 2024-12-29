from app import db
'''
數據層（模型）
職責：
表達書籍數據結構和邏輯。
負責與數據庫的交互（如查詢、插入、更新、刪除）。
用途：
定義書籍的數據結構，例如 ID、標題、作者等屬性。
處理數據的持久化。
'''
class Book(db.Model):
    __tablename__ = 'book'
    book_id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.Text,nullable = False)
    ISBN = db.Column(db.Text ,nullable = False)
    author = db.Column(db.Text ,nullable = False)
    version = db.Column(db.Text ,nullable = True) 
    public_year =  db.Column(db.Integer ,nullable = True) 
    publisher = db.Column(db.Text ,nullable = True) 
    create_time = db.Column(db.DateTime, default=db.func.current_timestamp())
    def to_dict(self):
        return {
            "book_id": self.book_id,
            "book_name": self.book_name,
            "ISBN": self.ISBN,
            "author": self.author,
            "version": self.version,
            "public_year": self.public_year,
            'publisher':self.publisher,
            "create_time": self.create_time.isoformat() if self.create_time else None 
        }