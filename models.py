# models.py
from datetime import datetime
from database import db

class Contact(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    phoneNumber = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=True)
    linkedId = db.Column(db.Integer, db.ForeignKey('contacts.id'), nullable=True)
    linkPrecedence = db.Column(db.String, default='primary')  # 'primary' or 'secondary'
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deletedAt = db.Column(db.DateTime, nullable=True)
