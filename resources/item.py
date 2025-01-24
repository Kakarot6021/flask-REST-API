# without usinfg schemas

# import uuid
# from db import items,stores
# from flask.views import MethodView
# from flask_smorest import abort,Blueprint
# from flask import request


# blp=Blueprint("items",__name__,description="Operations on items")

# @blp.route("/item/<string:item_id>")
# class Store(MethodView):
#     def get(self,item_id):
#         try:
#             return items[item_id]
#         except KeyError:
#             abort(404,message="Item not Found")

#     def delete(self,item_id):
#         try:
#             del items[item_id]
#             return "Item deleted."
#         except KeyError:
#             abort(404,message="item_id not found.")

#     def put(self,item_id):
#             request_data=request.get_json()
#             if "name" not in request_data or "price" not in request_data:
#                 abort(40098,message="Syntax is wrong.")
            
#             try:
#                 item=items[item_id]
#                 item |=request_data
#                 return item
#             except:
#                 abort(4049,message="Something went wrong.")          

# @blp.route("/item")
# class StoreList(MethodView):
#     def post(self):
#         item_data=request.get_json()
#         if("name" not in item_data or "price" not in item_data or "store_id" not in item_data ):
#             abort(400, message=" either name or price or store =_id not given. ")
        
#         for item in items.values():
#             if( item_data["name"]==item["name"] and item_data["store_id"]==item["store_id"]):
#                 abort(400, message="Item already exists.")

#         if item_data["store_id"] not in stores:
#             return "Store not found"
        
#         item_id=uuid.uuid4().hex
#         item={**item_data,"id" :item_id}
#         items[item_id]=item
        
#         return item

# using schemas



from db import db
from sqlalchemy.exc import SQLAlchemyError
from flask.views import MethodView
from flask_smorest import abort,Blueprint
from models import ItemModel,StoreModel
from  flask_jwt_extended import jwt_required,get_jwt

from schemas import ItemSchema,ItemUpdateSchema

blp=Blueprint("items",__name__,description="Operations on items")

@blp.route("/item/<string:item_id>")
class Store(MethodView):
    @jwt_required()
    @blp.response(202,ItemSchema)
    def get(self,item_id):
        item=ItemModel.query.get_or_404(item_id)
        return item
     
    @jwt_required()
    def delete(self,item_id):
         jwt=get_jwt()
         if not jwt.get("is_admin"):                       #jwt.get helsp us to check the data inside jwt 
                                                             #in this case it is whether it contains is_admin or not
             abort(404,message="Admin privelege required....")
         item=ItemModel.query.get_or_404(item_id)
         db.session.delete(item)
         db.session.commit()
         return {"message":"item deleted..."}
      
    @jwt_required()
    @blp.arguments(ItemUpdateSchema)
    @blp.response(201,ItemUpdateSchema)
    def put(self,request_data,item_id):
         item=ItemModel.query.get(item_id)
         if item:
            item.price=request_data["price"]
            item.name=request_data["name"]
         else:
             item=ItemModel(id=item_id,**request_data)   

         db.session.add(item)
         db.session.commit()
         return  item  
                     

@blp.route("/item")
class ItemList(MethodView):
    
    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201,ItemSchema)
    def post(self,item_data):
        # store = StoreModel.query.get(item_data["store_id"])
        # if ItemModel.query.filter_by(store_id=item_data["store_id"],name=item_data["name"]).first():
        #      abort(400,message="item already exist in store")
        item=ItemModel(**item_data)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            
            abort(500,message=str(e))
            
        return item
    
    @jwt_required()
    @blp.response(401,ItemSchema(many=True))
    def get(self):
        return  ItemModel.query.all()     #HERE ItemSchema(namy=true) converts it into list of items and query.all iterates though all items of list
    