from datetime import datetime
import json

from mongoengine import *
from MongographQL import MongraphSchema, Utils
import graphene


connect('MongraphQL')  # make sure to your mongodb is running, if isn't, run 'mongod' in terminal

class Posts(Document):
    title = StringField()
    text = StringField()
post1 = Posts(title="Post1", text="LOL")
post2 = Posts(title="Post2", text="HEY JOE")
post1.save()
post2.save()

class Country(Document):
    name = StringField()
    area_code = IntField()

brazil = Country(name="Brazil",
                 area_code=55)

class Bank(Document):
    name = StringField()
    country = ReferenceField(Country)

bank = Bank(name="Caixa",
            country=brazil)

class User(Document):
    username = StringField()
    password = StringField()
    active = BooleanField()
    age = IntField()
    score = FloatField()
    bank = ReferenceField(Bank)
    posts = ListField(ReferenceField(Posts))
    favorite_colors = ListField(StringField())
    creation_date = DateTimeField()
    site_url = URLField()
    location = PointField()

user = User(username="John",
            password="123456789",
            active=True,
            age=18,
            score=5.5,
            bank=bank,
            posts=[post1, post2],
            favorite_colors=['blue', 'red'],
            creation_date=datetime.now(),
            site_url="https://github.com/joaovitorsilvestre/MongographQL",
            location=[29.977291, 31.132493]
            )

brazil.save()
bank.save()
user.save()

class PostsSchema(metaclass=MongraphSchema):
    __MODEL__ = Posts

class CountrySchema(metaclass=MongraphSchema):
    __MODEL__ = Country

class BankSchema(metaclass=MongraphSchema):
    __MODEL__ = Bank
    __REF__ = {'country': CountrySchema}

class UserSchema(metaclass=MongraphSchema):
    __MODEL__ = User
    __REF__ = {'bank': BankSchema, 'posts': PostsSchema}

class Query(graphene.ObjectType):
    country = graphene.Field(CountrySchema, **CountrySchema.fields, resolver=CountrySchema.resolve_self)
    bank = graphene.Field(BankSchema, **BankSchema.fields, resolver=BankSchema.resolve_self)
    user = graphene.Field(UserSchema, **UserSchema.fields, resolver=UserSchema.resolve_self)

schema = graphene.Schema(query=Query)

result = schema.execute("""query Data {
    user(username: "John") {
        id
        username
        password
        active
        age
        score
        bank {
            name
            country {
                name
                areaCode
            }
        }
        posts {
            title
            text
        }
        favoriteColors
        creationDate
        siteUrl
        location
    }
}""")

parsed = {k: dict(v) for k, v in dict(result.data).items()}
print(json.dumps(parsed, indent=4, sort_keys=True))

user.delete()
bank.delete()
post1.delete()
post2.delete()
