from db import db  # Ensure db is initialized in your context

class ItemTags(db.Model):
    __tablename__ = "items_tags"

    id = db.Column(db.Integer, primary_key=True)
    items_id = db.Column(db.Integer, db.ForeignKey("items.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))
    store_id=db.Column(db.Integer,db.ForeignKey("stores.id"))
