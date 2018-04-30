def test_gen_mutation(mock_person):
    import graphene
    from graphene.utils.str_converters import to_snake_case
    from graphene.types.field import Field

    from graphene_mongodb.mutation import gen_mutation
    from graphene_mongodb.model import ModelSchema

    model_schema = ModelSchema(mock_person, mock_person._fields, None, None)

    result = gen_mutation(mock_person, model_schema.schema, model_schema.operators_mutation,
                          model_schema.fields_mutation, None, None)

    assert issubclass(result, graphene.Mutation)
    assert hasattr(result, 'mutate')

    assert result._meta.name == 'Create' + mock_person.__name__
    assert isinstance(result._meta.fields[to_snake_case(mock_person.__name__)], Field)

    assert result._meta.arguments == model_schema.operators_mutation


def test_gen_mutation_user_mutation_func(mock_person):
    import graphene
    from graphene_mongodb.mutation import gen_mutation
    from graphene_mongodb.model import ModelSchema

    def mutate(args, context):
        u = mock_person(**args)
        u.save()
        return u

    model_schema = ModelSchema(mock_person, mock_person._fields, mutate, None)

    user_mutate_func = gen_mutation(mock_person, model_schema.schema, model_schema.operators_mutation,
                          model_schema.fields_mutation, mutate, None)

    assert issubclass(user_mutate_func, graphene.Mutation)
    assert hasattr(user_mutate_func, 'mutate')
    assert getattr(user_mutate_func, 'mutate').__name__ == 'user_mutate'


def test_mutation_string_field(mock_person, schema_builder):
    from graphene_mongodb import MongoSchema
    from mongoengine import Document, StringField

    class Person(Document):
        name = StringField()

    class PersonSchema(MongoSchema):
        model = Person

        @staticmethod
        def mutate(args, context):
            u = Person(**args)
            u.save()
            return u

    schema = schema_builder([(PersonSchema, PersonSchema.single)], [PersonSchema])

    result = schema.execute("""mutation testMutation {
      createPerson(name: "John Armless") {
        person {
          name
        }
      }
    }""")

    assert not result.errors
    assert result.data == {'createPerson': {'person': {'name': 'John Armless'}}}


def test_mutation_boolean_field(mock_person, schema_builder):
    from graphene_mongodb import MongoSchema
    from mongoengine import Document, BooleanField

    class Person(Document):
        active = BooleanField()

    class PersonSchema(MongoSchema):
        model = Person

        @staticmethod
        def mutate(args, context):
            u = Person(**args)
            u.save()
            return u

    schema = schema_builder([(PersonSchema, PersonSchema.single)], [PersonSchema])

    result = schema.execute("""mutation testMutation {
      createPerson(active: true) {
        person {
          active
        }
      }
    }""")

    assert not result.errors
    assert result.data == {'createPerson': {'person': {'active': True}}}


def test_mutation_int_field(mock_person, schema_builder):
    from graphene_mongodb import MongoSchema
    from mongoengine import Document, IntField

    class Person(Document):
        age = IntField()

    class PersonSchema(MongoSchema):
        model = Person

        @staticmethod
        def mutate(args, context):
            u = Person(**args)
            u.save()
            return u

    schema = schema_builder([(PersonSchema, PersonSchema.single)], [PersonSchema])

    result = schema.execute("""mutation testMutation {
      createPerson(age: 21) {
        person {
          age
        }
      }
    }""")

    assert not result.errors
    assert result.data == {'createPerson': {'person': {'age': 21}}}


def test_mutation_float_field(mock_person, schema_builder):
    from graphene_mongodb import MongoSchema
    from mongoengine import Document, FloatField

    class Person(Document):
        score = FloatField()

    class PersonSchema(MongoSchema):
        model = Person

        @staticmethod
        def mutate(args, context):
            u = Person(**args)
            u.save()
            return u

    schema = schema_builder([(PersonSchema, PersonSchema.single)], [PersonSchema])

    result = schema.execute("""mutation testMutation {
      createPerson(score: 15.99) {
        person {
          score
        }
      }
    }""")

    assert not result.errors
    assert result.data == {'createPerson': {'person': {'score': 15.99}}}


def test_mutation_datetime_field(mock_person, schema_builder):
    from graphene_mongodb import MongoSchema
    from mongoengine import Document, DateTimeField
    from datetime import datetime

    class Person(Document):
        birthday = DateTimeField()

    class PersonSchema(MongoSchema):
        model = Person

        @staticmethod
        def mutate(args, context):
            u = Person(**args)
            u.save()
            return u

    schema = schema_builder([(PersonSchema, PersonSchema.single)], [PersonSchema])

    result = schema.execute("""mutation testMutation {
      createPerson(birthday: """ + '"{}"'.format(datetime(2018, 1, 1).isoformat()) + """) {
        person {
          birthday
        }
      }
    }""")

    assert not result.errors
    assert result.data == {'createPerson': {'person': {'birthday': datetime(2018, 1, 1).isoformat()}}}


def test_mutation_url_field(mock_person, schema_builder):
    from graphene_mongodb import MongoSchema
    from mongoengine import Document, URLField

    class Person(Document):
        site_url = URLField()

    class PersonSchema(MongoSchema):
        model = Person

        @staticmethod
        def mutate(args, context):
            u = Person(**args)
            u.save()
            return u

    schema = schema_builder([(PersonSchema, PersonSchema.single)], [PersonSchema])

    result = schema.execute("""mutation testMutation {
      createPerson(siteUrl: "http://www.deploydesexta.com.br") {
        person {
          siteUrl
        }
      }
    }""")

    assert not result.errors
    assert result.data == {'createPerson': {'person': {'siteUrl': 'http://www.deploydesexta.com.br'}}}


def test_dict_field(mock_person, schema_builder):
    from graphene_mongodb import MongoSchema
    from mongoengine import Document, DictField

    class Person(Document):
        book_info = DictField()

    class PersonSchema(MongoSchema):
        model = Person

        @staticmethod
        def mutate(args, context):
            u = Person(**args)
            u.save()
            return u

    schema = schema_builder([(PersonSchema, PersonSchema.single)], [PersonSchema])

    result = schema.execute("""mutation testMutation {
      createPerson(bookInfo: {title: "What if?"}) {
        person {
          bookInfo
        }
      }
    }""")

    assert not result.errors
    assert result.data == {'createPerson': {'person': {'bookInfo': {'title': 'What if?'}}}}


def test_email_field(mock_person, schema_builder):
    from graphene_mongodb import MongoSchema
    from mongoengine import Document, EmailField

    class Person(Document):
        email = EmailField()

    class PersonSchema(MongoSchema):
        model = Person

        @staticmethod
        def mutate(args, context):
            u = Person(**args)
            u.save()
            return u

    schema = schema_builder([(PersonSchema, PersonSchema.single)], [PersonSchema])

    result = schema.execute("""mutation testMutation {
      createPerson(email: "example@example.com.br") {
        person {
          email
        }
      }
    }""")

    assert not result.errors
    assert result.data == {'createPerson': {'person': {'email': 'example@example.com.br'}}}


def test_long_field(mock_person, schema_builder):
    from graphene_mongodb import MongoSchema
    from mongoengine import Document, LongField

    long = pow(2, 50) - 1

    class Person(Document):
        long = LongField()

    class PersonSchema(MongoSchema):
        model = Person

        @staticmethod
        def mutate(args, context):
            u = Person(**args)
            u.save()
            return u

    schema = schema_builder([(PersonSchema, PersonSchema.single)], [PersonSchema])

    result = schema.execute("""mutation testMutation {
      createPerson(long: """ + str(long) + """) {
        person {
          long
        }
      }
    }""")

    assert not result.errors
    assert result.data == {'createPerson': {'person': {'long': long}}}


def test_mutation_decimal_field(mock_person, schema_builder):
    from graphene_mongodb import MongoSchema
    from mongoengine import Document, DecimalField

    class Person(Document):
        remember_pi = DecimalField(precision=11, default=None)

    class PersonSchema(MongoSchema):
        model = Person

        @staticmethod
        def mutate(args, context):
            u = Person(**args)
            u.save()
            return u

    schema = schema_builder([(PersonSchema, PersonSchema.single)], [PersonSchema])

    result = schema.execute("""mutation testMutation {
      createPerson(rememberPi: 3.14159265359) {
        person {
          rememberPi
        }
      }
    }""")

    assert not result.errors
    assert result.data == {'createPerson': {'person': {'rememberPi': 3.14159265359}}}


def test_binary_field(mock_person, schema_builder):
    from graphene_mongodb import MongoSchema
    from mongoengine import Document, BinaryField

    class Person(Document):
        binary = BinaryField()
        binary2 = BinaryField()

    class PersonSchema(MongoSchema):
        model = Person

        @staticmethod
        def mutate(args, context):
            u = Person(**args)
            u.save()
            return u

    schema = schema_builder([(PersonSchema, PersonSchema.single)], [PersonSchema])

    result = schema.execute("""mutation testMutation {
      createPerson(binary: "Something", binary2: 50) {
        person {
          binary
          binary2
        }
      }
    }""")

    assert not result.errors
    assert result.data == {'createPerson': {'person': {'binary': 'Something', 'binary2': '50'}}}
