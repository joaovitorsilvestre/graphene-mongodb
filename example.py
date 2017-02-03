from mongoengine import *
from MongographQL import MongraphSchema, Utils
import graphene
import json

connect('MongraphQL')  # make sure to your mongodb is running, if isn't, run 'mongod' in terminal

class User(Document):
    username = StringField()
    password = StringField()

user = User(username="John", password="123456789")
user.save()

class UserSchema(metaclass=MongraphSchema):
    __MODEL__ = User

## OR (for more compability with Python 2.x)
# class UserSchema(Utils.with_metaclass(MongraphSchema, graphene.ObjectType)):
#     __MODEL__ = User

class Query(graphene.ObjectType):
    user = graphene.Field(UserSchema, **UserSchema.fields, resolver=UserSchema.resolve_self)

schema = graphene.Schema(query=Query)

result = schema.execute("""query Data {
    user(username: "John") {
        username
        password
    }
}""")

parsed = {k: dict(v) for k, v in dict(result.data).items()}
print(json.dumps(parsed, indent=4, sort_keys=True))
