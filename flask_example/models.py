from datetime import datetime

from mongoengine import *


class Post(Document):
    title = StringField()
    text = StringField()


class Bank(Document):
    name = StringField()
    location = PointField()


class User(Document):
    username = StringField()
    active = BooleanField()
    age = IntField()
    score = FloatField()
    bank = ReferenceField(Bank)
    posts = ListField(ReferenceField(Post))
    favorite_colors = ListField(StringField())
    creation_date = DateTimeField()
    site_url = URLField()
    personal_data = DictField()
    email = EmailField()
    super_id = LongField()
    remember_pi = DecimalField(min_value=3.1, max_value=3.15, precision=11)
    ordered_favorite_colors = SortedListField(StringField())
    nickname = BinaryField()
