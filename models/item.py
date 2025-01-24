from db import db  # Make sure db is initialized correctly in your app context
from models.item_tags import ItemTags

class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description=db.Column(db.String)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=True, nullable=False)
    store = db.relationship("StoreModel", back_populates="items")
    
    # Use string references to avoid early evaluation
    tags = db.relationship("TagModel", back_populates="items", secondary="items_tags")
