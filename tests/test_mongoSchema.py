import json
from collections import OrderedDict

import graphene
from mongoengine import *
from MongographQL import MongraphSchema

connect('MongraphQL-Tests')

def generate_query_result(fields):
    attrs = {name: graphene.Field(schema, **schema.fields, resolver=schema.resolver_self)
             for name, schema in fields.items()}

    subclass = type('Query', (graphene.ObjectType,), attrs)
    return subclass

def execute_query(schema, query):
    _query = generate_query_result({'user': schema})
    _schema = graphene.Schema(query=_query)
    return json.loads(json.dumps(_schema.execute(query).data))

def test_MongoSchema_string():
    class User(Document):
        name = StringField()

    class UserSchema(metaclass=MongraphSchema):
        __MODEL__ = User

    user = User(name="John")
    user.save()

    result = execute_query(UserSchema,
                           """ query testQuery {
                               user(name: "John") {
                                   name
                               }
                           }""")

    assert result == {"user": {"name": "John"}}
    user.delete()

def test_MongoSchema_float():
    class User(Document):
        score = FloatField()

    class UserSchema(metaclass=MongraphSchema):
        __MODEL__ = User

    user = User(score=15.684520)
    user.save()

    result = execute_query(UserSchema,
                           """ query testQuery {
                               user(score: 15.684520) {
                                   score
                               }
                           }""")

    assert result == {"user": {"score": 15.684520}}
    user.delete()


def test_MongoSchema_int():
    class User(Document):
        age = IntField()

    class UserSchema(metaclass=MongraphSchema):
        __MODEL__ = User

    user = User(age=19)
    user.save()

    result = execute_query(UserSchema,
                           """ query testQuery {
                               user(age: 19) {
                                   age
                               }
                           }""")

    assert result == {"user": {"age": 19}}
    user.delete()

def test_MongoSchema_id():
    class User(Document):
        pass

    class UserSchema(metaclass=MongraphSchema):
        __MODEL__ = User

    user = User()
    user.save()
    user_from_db = User.objects().first()

    result = execute_query(UserSchema,
                           """ query testQuery {
                               user {
                                   id
                               }
                           }""")

    assert result == {"user": {"id": str(user_from_db.id)}}
    user_from_db.delete()

def test_MongoSchema_boolean():
    class User(Document):
        active = BooleanField()
        not_active = BooleanField()

    class UserSchema(metaclass=MongraphSchema):
        __MODEL__ = User

    user = User(active=False, not_active=True)
    user.save()

    result = execute_query(UserSchema,
                           """ query testQuery {
                               user {
                                   active
                                   notActive
                               }
                           }""")

    assert result == {"user": {"active": False, "notActive": True}}
    user.delete()

def test_MongoSchema_referenceField():
    class Bank(Document):
        name = StringField()

    class User(Document):
        bank = ReferenceField(Bank)

    class Bankchema(metaclass=MongraphSchema):
        __MODEL__ = Bank

    class UserSchema(metaclass=MongraphSchema):
        __MODEL__ = User
        __REF__ = {'bank': Bankchema}

    bank = Bank(name="Test Bank")
    user = User(bank=bank)

    bank.save()
    user.save()

    result = execute_query(UserSchema,
                           """ query testQuery {
                               user {
                                   bank {
                                       name
                                   }
                               }
                           }""")

    assert result == {"user": {"bank": {"name": "Test Bank"}}}
    user.delete()
    bank.delete()
