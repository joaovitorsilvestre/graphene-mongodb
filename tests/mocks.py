import pytest
from datetime import datetime
from mongoengine import *


@pytest.fixture(scope="function")
def mock_post(mongo):
    class Post(Document):
        text = StringField()

    yield Post

@pytest.fixture(scope="function")
def mock_person(mongo, mock_post):
    """ Create a mock for person """

    class Person(Document):
        name = StringField(default=None)
        active = BooleanField(default=None)
        age = IntField(default=None)
        score = FloatField(default=None)
        birthday = DateTimeField(default=None)
        site_url = URLField(default=None)
        book_info = DictField(default=None)
        email = EmailField(default=None)
        super_id = LongField(default=None)
        remember_pi = DecimalField(min_value=3.1, max_value=3.15, precision=11, default=None)
        nickname = BinaryField(default=None)
        location = PointField(default=None)
        favourite_colors = ListField(StringField(), default=None)
        posts = ListField(ReferenceField(mock_post), default=None)
        best_post = ReferenceField(mock_post, default=None)

    yield Person

@pytest.fixture(scope="function")
def mock_person_filled(mongo, mock_post):
    """ Create a mock for person """

    post1 = mock_post(text="Hey Joe")
    post2 = mock_post(text="Say my name")
    post1.save()
    post2.save()

    class Person(Document):
        name = StringField(default="John Travolta")
        active = BooleanField(default=True)
        age = IntField(default=20)
        score = FloatField(default=5.0)
        birthday = DateTimeField(default=datetime.now())
        site_url = URLField(default="http://www.test.com.br")
        book_info = DictField(default={'author': 'John'})
        email = EmailField(default='john@test.com.br')
        super_id = LongField(default=pow(2, 63) - 1)
        remember_pi = DecimalField(min_value=3.1, max_value=3.15, precision=11, default=3.14159265359)
        nickname = BinaryField(default=b"John Armless")
        location = PointField(default=[29.977291, 31.132493])
        favourite_colors = ListField(StringField(), default=['red', 'blue'])
        posts = ListField(ReferenceField(mock_post), default=[post1, post2])
        best_post = ReferenceField(mock_post, default=post1)

    yield Person


