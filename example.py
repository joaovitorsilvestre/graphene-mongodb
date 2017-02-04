import json

from mongoengine import *
from MongographQL import MongraphSchema
import graphene


connect('MongraphQL')  # make sure to your mongodb is running, if isn't, run 'mongod' in terminal

class User(Document):
    username = StringField()
    password = StringField()
    active = BooleanField()
    age = IntField()
    score = FloatField()

user = User(username="John",
            password="123456789",
            active=True,
            age=18,
            score=5.5)
user.save()

class UserSchema(metaclass=MongraphSchema):
    __MODEL__ = User

class Query(graphene.ObjectType):
    user = graphene.Field(UserSchema, **UserSchema.fields, resolver=UserSchema.resolve_self)

schema = graphene.Schema(query=Query)

result = schema.execute("""query Data {
    user(username: "John") {
        username
        password
        active
        age
        score
    }
}""")

parsed = {k: dict(v) for k, v in dict(result.data).items()}
print(json.dumps(parsed, indent=4, sort_keys=True))
user.delete()
