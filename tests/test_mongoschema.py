from datetime import datetime
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
