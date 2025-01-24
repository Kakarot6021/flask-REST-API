from flask.views import MethodView
from flask_smorest import Blueprint,abort
from sqlalchemy.exc import SQLAlchemyError

import uuid
# from db import stores
from flask.views import MethodView
from flask_smorest import abort,Blueprint

from models import StoreModel
from schemas import StoreSchema
from db import db
from sqlalchemy.exc import IntegrityError,SQLAlchemyError
import traceback
from flask import jsonify

from db import db
from models import TagModel,StoreModel,ItemModel
from schemas import TagSchema,TagAndItemSchema

blp=Blueprint("Tags","tags",description="Operations on tags")

@blp.route("/store/<string:store_id>/tag")
class TagsInStore(MethodView):
    @blp.response(200,TagSchema(many=True))
    def get(self,store_id):
        store=StoreModel.query.get_or_404(store_id)
        
        return store.tags.all()      #in store model it is laxy so we have pass it as querry.
    
    @blp.arguments(TagSchema)
    @blp.response(200,TagSchema)
    def post(self,tag_data,store_id):
        # if TagModel.query.filter(TagModel.store_id==store_id, TagModel.name==tag_data["name"]).first():
        #     abort(400,message="Tag with same id alresy exists in the store.")

        tag=TagModel(**tag_data,store_id=store_id)

        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500,message=str(e))

        return tag       
@blp.route("/store/<string:store_id>/tag/<string:tag_id>")
class LinkTagsToItem(MethodView):
    @blp.response(202,TagSchema)
    def post(self,item_id,tag_id):
        item=ItemModel.query.get_or_404(item_id)
        tag=TagModel.query.get_or_404(tag_id)

        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(404,message="An Error occured... while inserting the tag")

        return tag    


    @blp.response(202,TagAndItemSchema)   #here we are unlinking the tag
    def delete(self,item_id,tag_id):
        item=ItemModel.query.get_or_404(item_id)
        tag=TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(404,message="An Error occured... while deleting the tag")

        return {"message":"Item removed from tag","item": item,"tag":tag}    

@blp.route("/tag/<string:tag_id>")
class Tag(MethodView):
    @blp.response(200,TagSchema)
    def get(self,tag_id):
        tag=TagModel.query.get_or_404(tag_id)
        return tag
    
    @blp.response(202,
                  description="Delete a tag if no item is tagged with it",
                  example={"mesage":"Tag Deleted"})
    @blp.alt_response(404,description="TAg not found")
    def delete(self,tag_id):
        tag=TagModel.query.get_or_404(tag_id)

        if not tag.item:
            db.session.delete(tag)
            db.session.commit()
            return {"message":"tag Deleted"}
