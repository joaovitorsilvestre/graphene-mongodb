from mongoengine import *
from MongographQL import MongraphSchema, Utils
import graphene
import json

connect('MongraphQL')  # make sure to your mongodb is running, if isn't, run 'mongod' in terminal

class Bank(Document):
    name = StringField()

bank = Bank(name="Caixa")
bank.save()

class User(Document):
    username = StringField()
    password = StringField()
    active = BooleanField()
    age = IntField()
    score = FloatField()
    bank = ReferenceField(Bank)


user = User(username="John",
            password="123456789",
            active=True,
            age=18,
            score=5.5,
            bank=bank)
user.save()

class BankSchema(metaclass=MongraphSchema):
    __MODEL__ = Bank

class UserSchema(metaclass=MongraphSchema):
    __MODEL__ = User
    __REF__ = {'bank': BankSchema}

class Query(graphene.ObjectType):
    user = graphene.Field(UserSchema, **UserSchema.fields, resolver=UserSchema.resolve_self)
    bank = graphene.Field(BankSchema, **BankSchema.fields, resolver=BankSchema.resolve_self)

schema = graphene.Schema(query=Query)

result = schema.execute("""query Data {
    user(username: "John") {
        username
        password
        active
        age
        score
        bank {
            name
        }
    }
}""")

parsed = {k: dict(v) for k, v in dict(result.data).items()}
print(json.dumps(parsed, indent=4, sort_keys=True))

user.delete()
bank.delete()
