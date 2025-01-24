from db import db

class  StoreModel(db.Model):
    __tablename__="stores"

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(80),unique=False,nullable=False)
    items=db.relationship("ItemModel",back_populates="store",lazy="dynamic",cascade ="all,delete") #dynamic means that it does not create items query unless we tell it to.. 
     # we use cascade to delete all the items once a store is deleted....oterwise item file will tyy to make store_id null but it is nullable .//so error will come
    
    tags=db.relationship("TagModel",back_populates="store",lazy="dynamic") #here "store is the name of realtionship defined in the tag.py" 
    #tags = db.relationship("ItemTags", back_populates="store")


   