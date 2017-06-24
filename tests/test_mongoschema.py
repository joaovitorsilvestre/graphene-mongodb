from tests.utils import MongographQLTestCase
from mongoengine import *

from MongographQL import MongraphSchema
import graphene


class FieldsTest(MongographQLTestCase):

    def test_string_field(self):
        class Person(Document):
            name = StringField()

        class PersonSchema(MongraphSchema):
            __MODEL__ = Person

        Person(name="John").save()

        Query = self.QueryBuilder([PersonSchema])
        schema = graphene.Schema(query=Query)

        result = schema.execute(""" query testQuery {
           person(name: "John") {
               name
           }
        }""")

        assert result.data == {'person': {'name': 'John'}}

    def test_boolean_field(self):
        class Person(Document):
            is_good_person = BooleanField()

        class PersonSchema(MongraphSchema):
            __MODEL__ = Person

        Person(is_good_person=True).save()

        Query = self.QueryBuilder([PersonSchema])
        schema = graphene.Schema(query=Query)

        result = schema.execute(""" query testQuery {
           person(isGoodPerson: true) {
               isGoodPerson
           }
        }""")

        assert result.data == {'person': {'isGoodPerson': True}}

    def test_int_field(self):
        class Person(Document):
            age = IntField()

        class PersonSchema(MongraphSchema):
            __MODEL__ = Person

        Person(age=19).save()

        Query = self.QueryBuilder([PersonSchema])
        schema = graphene.Schema(query=Query)

        result = schema.execute(""" query testQuery {
           person(age: 19) {
               age
           }
        }""")

        assert result.data == {'person': {'age': 19}}

    def test_float_field(self):
        class Person(Document):
            score = FloatField()

        class PersonSchema(MongraphSchema):
            __MODEL__ = Person

        Person(score=9.5).save()

        Query = self.QueryBuilder([PersonSchema])
        schema = graphene.Schema(query=Query)

        result = schema.execute(""" query testQuery {
           person(score: 9.5) {
               score
           }
        }""")

        assert result.data == {'person': {'score': 9.5}}

    def test_datetime_field(self):
        from datetime import datetime

        class Person(Document):
            birth = DateTimeField()

        class PersonSchema(MongraphSchema):
            __MODEL__ = Person

        birth = datetime.now()
        Person(birth=birth).save()

        Query = self.QueryBuilder([PersonSchema])
        schema = graphene.Schema(query=Query)

        birth_expected = Person.objects(birth=birth).first().birth

        result = schema.execute(""" query testQuery {
            person {
                birth
            }
        }""")

        assert result.data == {'person': {'birth': birth_expected.isoformat()}}

    def test_id_field(self):
        class Person(Document):
            pass

        class PersonSchema(MongraphSchema):
            __MODEL__ = Person

        person = Person()
        person.save()
        person_from_db = Person.objects().first()

        Query = self.QueryBuilder([PersonSchema])
        schema = graphene.Schema(query=Query)

        result = schema.execute(""" query testQuery {
           person {
               id
           }
        }""")

        assert result.data == {'person': {'id': str(person_from_db.id)}}

    def test_url_field(self):
        class Site(Document):
            url = URLField()

        class SiteSchema(MongraphSchema):
            __MODEL__ = Site

        url = "https://github.com/joaovitorsilvestre/MongographQL"
        Site(url=url).save()

        Query = self.QueryBuilder([SiteSchema])
        schema = graphene.Schema(query=Query)

        result = schema.execute(""" query testQuery {
            site {
                url
            }
        }""")

        assert result.data == {'site': {'url': url}}

    def test_dict_field(self):
        class Post(Document):
            info = DictField()

        info = {
            "author": "João",
            "date": "2017-01-01"
        }

        Post(info=info).save()

        class PostSchema(MongraphSchema):
            __MODEL__ = Post

        Query = self.QueryBuilder([PostSchema])
        schema = graphene.Schema(query=Query)

        result = schema.execute(""" query testQuery {
            post {
                info
            }
        }""")

        assert result.data == {'post': {'info': info}}

    def test_email_field(self):
        class User(Document):
            email = EmailField()

        User(email="email@server.com").save()

        class UserSchema(MongraphSchema):
            __MODEL__ = User

        Query = self.QueryBuilder([UserSchema])
        schema = graphene.Schema(query=Query)

        result = schema.execute(""" query testQuery {
            user {
                email
            }
        }""")

        assert result.data == {'user': {'email': 'email@server.com'}}

    def test_long_field(self):
        class User(Document):
            super_id = LongField()

        User(super_id=9223372036854775807).save()

        class UserSchema(MongraphSchema):
            __MODEL__ = User

        Query = self.QueryBuilder([UserSchema])
        schema = graphene.Schema(query=Query)

        result = schema.execute(""" query testQuery {
            user {
                superId
            }
        }""")

        assert result.data == {'user': {'superId': 9223372036854775807}}

    def test_decimal_field(self):
        class Person(Document):
            remember_pi = DecimalField(min_value=3.1, max_value=3.15, precision=11)

        Person(remember_pi=3.14159265359).save()

        class PersonSchema(MongraphSchema):
            __MODEL__ = Person

        Query = self.QueryBuilder([PersonSchema])
        schema = graphene.Schema(query=Query)

        result = schema.execute(""" query testQuery {
                    person {
                        rememberPi
                    }
                }""")

        assert result.data == {'person': {'rememberPi': 3.14159265359}}

    def test_binaty_field(self):
        class Person(Document):
            nickname = BinaryField()

        Person(nickname=b"John armless").save()

        class PersonSchema(MongraphSchema):
            __MODEL__ = Person

        Query = self.QueryBuilder([PersonSchema])
        schema = graphene.Schema(query=Query)

        result = schema.execute(""" query testQuery {
            person {
                nickname
            }
        }""")

        assert result.data == {'person': {'nickname': "John armless"}}

    def test_point_field(self):
        class Bank(Document):
            location = PointField()

        Bank(location=[29.977291, 31.132493]).save()

        class BankSchema(MongraphSchema):
            __MODEL__ = Bank

        Query = self.QueryBuilder([BankSchema])
        schema = graphene.Schema(query=Query)

        result = schema.execute(""" query testQuery {
            bank {
                location
            }
        }""")

        assert result.data == {'bank':
                                   {'location': {
                                       "type": "Point",
                                       "coordinates": [29.977291, 31.132493]
                                   }}
                               }

    def test_list_field(self):
        class Person(Document):
            favourite_colors = ListField(StringField())

        Person(favourite_colors=["blue", "red"]).save()

        class PersonSchema(MongraphSchema):
            __MODEL__ = Person

        Query = self.QueryBuilder([PersonSchema])
        schema = graphene.Schema(query=Query)

        result = schema.execute(""" query testQuery {
            person {
                favouriteColors
            }
        }""")

        assert result.data == {'person': {'favouriteColors': ["blue", "red"]}}

    def test_list_reference_field(self):
        class Post(Document):
            text = StringField()

        class Person(Document):
            posts = ListField(ReferenceField(Post))

        post1 = Post(text="Hey Joe")
        post2 = Post(text="Say my name")
        post1.save()
        post2.save()

        Person(posts=[post1, post2]).save()

        class PersonSchema(MongraphSchema):
            __MODEL__ = Person

        Query = self.QueryBuilder([PersonSchema])
        schema = graphene.Schema(query=Query)

        result = schema.execute(""" query testQuery {
            person {
                posts {
                    text
                }
            }
        }""")

        assert result.data == {'person': {
            'posts': [
                {"text": "Hey Joe"},
                {"text": "Say my name"}
            ]
        }}

    def test_reference_field(self):
        class Bank(Document):
            name = StringField()

        caixa = Bank(name="Caixa")
        caixa.save()

        class Person(Document):
            bank = ReferenceField(Bank)

        Person(bank=caixa).save()

        class PersonSchema(MongraphSchema):
            __MODEL__ = Person

        Query = self.QueryBuilder([PersonSchema])
        schema = graphene.Schema(query=Query)

        result = schema.execute(""" query testQuery {
            person {
                bank {
                    name
                }
            }
        }""")

        assert result.data == {'person': {
            'bank': {
                'name': 'Caixa'
            }
        }}

    def test_auto_resolver_list(self):
        class User(Document):
            name = StringField()

        User(name="Ross").save()
        User(name="Chandler").save()
        User(name="Joey").save()

        class UserSchema(MongraphSchema):
            __MODEL__ = User

        class Query(graphene.ObjectType):
            users = UserSchema.list()

        schema = graphene.Schema(query=Query)

        result = schema.execute(""" query testQuery {
            users {
                name
            }
        }""")

        assert result.data == {'users': [
            {'name': 'Ross'},
            {'name': 'Chandler'},
            {'name': 'Joey'}
        ]}

    def test_model_missing(self):
        def gen_schema():
            return type('PersonSchema', (MongraphSchema,), {})

        self.assertRaises(AttributeError, gen_schema)


    def test_model_wrong_type(self):
        class Person(object):
            pass

        def gen_schema():
            return type('PersonSchema', (MongraphSchema,), {'__MODEL__': Person})

        self.assertRaises(TypeError, gen_schema)




