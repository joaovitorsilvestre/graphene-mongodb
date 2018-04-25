from datetime import datetime

import graphene
from graphene_mongodb import MongoSchema
from .models import User, Bank, Post


def verify_permission(model, fields, query, special_params):
    try:
        print(model, fields, query, special_params)
        assert True
    except Exception:
        raise Exception('Unauthorized Access')


class PostSchema(MongoSchema):
    model = Post


class BankSchema(MongoSchema):
    model = Bank


class UserSchema(MongoSchema):
    model = User
    validator = verify_permission

    @staticmethod
    def mutate(args, context):
        # context is the flask global request
        u = User(**args)
        u.creation_date = datetime.now()
        u.save()
        return u


class Person(graphene.ObjectType):
    name = graphene.String()
    age = graphene.Int()


class Query(graphene.ObjectType):
    user = UserSchema.single
    bank = BankSchema.single
    post = PostSchema.single
    posts = PostSchema.list


class Mutation(graphene.ObjectType):
    create_user = UserSchema.mutate

schema = graphene.Schema(query=Query, mutation=Mutation)


def save_tests_in_db():
    post1 = Post(title="Post1", text="LOL")
    post2 = Post(title="Post2", text="HEY JOE")
    post1.save()
    post2.save()

    bank = Bank(name="Caixa", location=[29.977291, 31.132493])
    bank.save()

    user = User(username="John",
                active=True,
                age=18,
                score=5.5,
                bank=bank,
                posts=[post1, post2],
                favorite_colors=['blue', 'red'],
                creation_date=datetime.now(),
                site_url="https://github.com/joaovitorsilvestre/MongographQL",
                personal_data={"fullName": "John John",
                               "passport": 15874512354,
                               "children_names": ["Ross", "Chandler"]},
                email="John@server.com",
                super_id=9223372036854775807,
                remember_pi=3.14159265359,
                ordered_favorite_colors=['red', 'blue'],
                nickname=b'John armless'
                )
    user.save()
