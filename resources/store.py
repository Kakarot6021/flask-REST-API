import uuid
# from db import stores
from flask.views import MethodView
from flask_smorest import abort,Blueprint
from flask import request
from models import StoreModel
from schemas import StoreSchema
from db import db
from sqlalchemy.exc import IntegrityError,SQLAlchemyError
import traceback
from flask import jsonify


blp=Blueprint("stores",__name__,description="Operations on stores")

@blp.route("/store/<string:store_id>")
class Store(MethodView):
    @blp.response(200,StoreSchema)
    def get(self,store_id):
        store=StoreModel.query.get_or_404(store_id)
        return store

    def delete(self,store_id):
        store=StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message":"Store deleted"}

@blp.route("/store")
class StoreList(MethodView):
    @blp.arguments(StoreSchema)
    @blp.response(201,StoreSchema)
    def post(self,store_data):
        store=StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(303,message="This store alresy exists..")
        except SQLAlchemyError:
            abort(505,message="something went wrong...")    
           
        return store
    
    @blp.response(200,StoreSchema(many=True))
    def get(self):
        try:
         return StoreModel.query.all()
        except Exception as e:
            return jsonify({
            'error': 'Unexpected error',
            'message': str(e),
            'trace': traceback.format_exc()
        }), 500