from graphene_mongodb import MongoSchema


def test_string_field(schema_builder, mock_person):
    p = mock_person(name="John")
    p.save()
    PersonSchema = MongoSchema(mock_person)

    schema = schema_builder([(PersonSchema, PersonSchema.single)])
    result = schema.execute(""" query testQuery {
       person {
           name
       }
    }""")

    assert not result.errors
    assert result.data == {'person': {'name': p.name}}


def test_boolean_field(mock_person, schema_builder):
    p = mock_person(active=True)
    p.save()
    PersonSchema = MongoSchema(mock_person)

    schema = schema_builder([(PersonSchema, PersonSchema.single)])
    result = schema.execute(""" query testQuery {
       person {
           active
       }
    }""")

    assert result.data == {'person': {'active': p.active}}


def test_int_field(mock_person, schema_builder):
    p = mock_person(age=20)
    p.save()
    PersonSchema = MongoSchema(mock_person)

    schema = schema_builder([(PersonSchema, PersonSchema.single)])
    result = schema.execute(""" query testQuery {
       person {
           age
       }
    }""")

    assert result.data == {'person': {'age': p.age}}


def test_float_field(mock_person, schema_builder):
    p = mock_person(score=9.5)
    p.save()
    PersonSchema = MongoSchema(mock_person)

    schema = schema_builder([(PersonSchema, PersonSchema.single)])
    result = schema.execute(""" query testQuery {
       person {
           score
       }
    }""")

    assert result.data == {'person': {'score': p.score}}


def test_datetime_field(mock_person, schema_builder):
    from datetime import datetime

    birth = datetime(2017, 1, 1)
    p = mock_person(birthday=birth).save()
    p.save()
    PersonSchema = MongoSchema(mock_person)


    schema = schema_builder([(PersonSchema, PersonSchema.single)])
    result = schema.execute(""" query testQuery {
         person {
             birthday
         }
     }""")

    assert result.data == {'person': {'birthday': birth.isoformat()}}
    assert result.data == {'person': {'birthday': p.birthday.isoformat()}}


def test_id_field(mock_person, schema_builder):
    p = mock_person()
    p.save()
    PersonSchema = MongoSchema(mock_person)

    schema = schema_builder([(PersonSchema, PersonSchema.single)])
    result = schema.execute(""" query testQuery {
       person {
           id
       }
    }""")

    assert result.data == {'person': {'id': str(p.id)}}


def test_url_field(mock_person, schema_builder):
    site_url = "https://github.com/joaovitorsilvestre/MongographQL"

    p = mock_person(site_url=site_url)
    p.save()
    PersonSchema = MongoSchema(mock_person)

    schema = schema_builder([(PersonSchema, PersonSchema.single)])
    result = schema.execute(""" query testQuery {
        person {
            siteUrl
        }
    }""")

    assert result.data == {'person': {'siteUrl': p.site_url}}
    assert result.data == {'person': {'siteUrl': site_url}}


def test_dict_field(mock_person, schema_builder):
    info = {
        "author": "João",
        "date": "2017-01-01"
    }

    p = mock_person(book_info=info)
    p.save()

    PersonSchema = MongoSchema(mock_person)

    schema = schema_builder([(PersonSchema, PersonSchema.single)])
    result = schema.execute(""" query testQuery {
        person {
            bookInfo
        }
    }""")

    assert result.data == {'person': {'bookInfo': info}}
    assert result.data == {'person': {'bookInfo': p.book_info}}


def test_email_field(mock_person, schema_builder):
    p = mock_person(email="test@test.com.br")
    p.save()
    PersonSchema = MongoSchema(mock_person)

    schema = schema_builder([(PersonSchema, PersonSchema.single)])
    result = schema.execute(""" query testQuery {
        person {
            email
        }
    }""")

    assert result.data == {'person': {'email': p.email}}


def test_long_field(mock_person, schema_builder):
    long = pow(2, 63) - 1
    p = mock_person(super_id=long)
    p.save()
    PersonSchema = MongoSchema(mock_person)

    schema = schema_builder([(PersonSchema, PersonSchema.single)])
    result = schema.execute(""" query testQuery {
        person {
            superId
        }
    }""")

    assert result.data == {'person': {'superId': long}}
    assert result.data == {'person': {'superId': p.super_id}}


def test_decimal_field(mock_person, schema_builder):
    p = mock_person(remember_pi=3.14159265359)
    p.save()
    PersonSchema = MongoSchema(mock_person)

    schema = schema_builder([(PersonSchema, PersonSchema.single)])
    result = schema.execute(""" query testQuery {
        person {
            rememberPi
        }
    }""")

    assert result.data == {'person': {'rememberPi': float(p.remember_pi)}}


def test_binary_field(mock_person, schema_builder):
    p = mock_person(nickname=b"John armless")
    p.save()
    PersonSchema = MongoSchema(mock_person)

    schema = schema_builder([(PersonSchema, PersonSchema.single)])
    result = schema.execute(""" query testQuery {
        person {
            nickname
        }
    }""")

    assert result.data == {'person': {'nickname': p.nickname.decode('utf-8')}}


def test_point_field(mock_person, schema_builder):
    p = mock_person(location=[29.977291, 31.132493])
    p.save()
    PersonSchema = MongoSchema(mock_person)

    schema = schema_builder([(PersonSchema, PersonSchema.single)])
    result = schema.execute(""" query testQuery {
        person {
            location
        }
    }""")

    assert result.data == {'person':
                               {'location': {
                                   "type": "Point",
                                   "coordinates": [29.977291, 31.132493]
                               }}
                           }


def test_list_field(mock_person, schema_builder):
    p = mock_person(favourite_colors=['blue', 'red'])
    p.save()
    PersonSchema = MongoSchema(mock_person)

    schema = schema_builder([(PersonSchema, PersonSchema.single)])
    result = schema.execute(""" query testQuery {
        person {
            favouriteColors
        }
    }""")

    assert result.data == {'person': {'favouriteColors': p.favourite_colors}}


def test_list_reference_field(mock_person, mock_post, schema_builder):
    post1 = mock_post(text="Hey Joe")
    post2 = mock_post(text="Say my name")
    post1.save()
    post2.save()

    mock_person(posts=[post1, post2]).save()
    PersonSchema = MongoSchema(mock_person)

    schema = schema_builder([(PersonSchema, PersonSchema.single)])
    result = schema.execute(""" query testQuery {
        person {
            posts {
                text
            }
        }
    }""")

    assert result.data == {'person': {
        'posts': [
            {"text": post1.text},
            {"text": post2.text}
        ]
    }}


def test_reference_field(mock_person, mock_post, schema_builder):
    post = mock_post(text="Hey Joe")
    post.save()

    mock_person(best_post=post).save()
    PersonSchema = MongoSchema(mock_person)

    schema = schema_builder([(PersonSchema, PersonSchema.single)])
    result = schema.execute(""" query testQuery {
        person {
            bestPost {
                text
            }
        }
    }""")

    assert result.data == {'person': {
        'bestPost': {
            'text': post.text
        }
    }}