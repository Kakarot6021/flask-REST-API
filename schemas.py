from marshmallow import Schema,fields

class PlainItemSchema(Schema):
    id=fields.Int(dump_only=True)   #dump_only is for only recieving dat an we only use it to returnng data written in diary.
    name=fields.Str(required=True)
    price=fields.Float(required=True)
   

class ItemUpdateSchema(Schema):
    name=fields.Str()
    price=fields.Float()
    store_id=fields.Int()

class PlainStoreSchema(Schema):
    id=fields.Int(dump_only=True)
    name=fields.Str(required=True)

class PlaintagSchema(Schema):
     id=fields.Int(dump_only=True)
     name=fields.Str(required=True)


class ItemSchema(PlainItemSchema):
     store_id=fields.Int(required=True,load_only=True)
     store=fields.Nested(PlainStoreSchema,dump_only=True) #only returning data to the client and not recieving it
     tags=fields.Nested(PlaintagSchema,dump_only=True)


class StoreSchema(PlainStoreSchema):
      items=fields.List(fields.Nested(PlainItemSchema()),dump_only=True)
      tags=fields.List(fields.Nested(PlaintagSchema()),dump_only=True)
      

  


class TagSchema(PlaintagSchema):
     store_id=fields.Int(load_only=True)
     store=fields.Nested(PlainStoreSchema(),dump_only=True)
     items=fields.List(fields.Nested(PlainItemSchema()),dump_only=True)

class TagAndItemSchema(Schema):
     message=fields.Str()
     item=fields.Nested(ItemSchema)
     tag=fields.Nested(TagSchema)
     
class userSchema(Schema):
     id=fields.Int(load_only=True)
     username=fields.Str(required=True)
     password=fields.Str(required=True,load_only=True) #most imporatant thing we have done.password can never be shown to the client