from datetime import datetime

import graphene
from MongographQL import MongraphSchema
from .models import User, Bank, Post


class PostSchema(MongraphSchema):
    model = Post


class BankSchema(MongraphSchema):
    model = Bank


class UserSchema(MongraphSchema):
    model = User


class Query(graphene.ObjectType):
    user = UserSchema.single()
    bank = BankSchema.single()
    post = PostSchema.single()
    posts = PostSchema.list()

schema = graphene.Schema(query=Query)


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
