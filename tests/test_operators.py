from MongographQL import MongraphSchema


query = lambda operators: """ query testQuery {
        person(%s) {
            id
            name            
            active 
            age 
            score 
            birthday 
            siteUrl 
            bookInfo 
            email 
            superId 
            rememberPi 
            nickname 
            location
            favouriteColors 
            posts {
                id
                text
            }
            bestPost {
                id
                text
            } 
        }
    }""" % operators


def test_no_operator(schema_builder, mock_person_filled):
    """ without operator we consider that is a string with an id """
    p = mock_person_filled()
    p.save()
    PersonSchema = MongraphSchema(mock_person_filled)

    schema = schema_builder([PersonSchema])
    result = schema.execute(query('id:"' + str(p.id) + '"'))

    assert result.data['person']['id'] == str(p.id)


def test_in(schema_builder, mock_person_filled):
    p = mock_person_filled()
    p.save()
    PersonSchema = MongraphSchema(mock_person_filled)

    schema = schema_builder([PersonSchema])
    result = schema.execute(query('id_In:["' + str(p.id) + '"]'))

    assert result.data['person']['id'] == str(p.id)


def test_nin(schema_builder, mock_person_filled, mock_person):
    p1 = mock_person_filled()
    p2 = mock_person()
    p1.save()
    p2.save()
    PersonSchema = MongraphSchema(mock_person_filled)

    schema = schema_builder([PersonSchema])
    result = schema.execute(query('id_Nin:["' + str(p1.id) + '"]'))

    assert result.data['person']['id'] != str(p1.id)
    assert result.data['person']['id'] == str(p2.id)


def test_exact(schema_builder, mock_person_filled):
    p = mock_person_filled()
    p.save()
    PersonSchema = MongraphSchema(mock_person_filled)

    schema = schema_builder([PersonSchema])

    result = schema.execute(query('name_Exact:"' + p.name + '"'))
    assert result.data['person']['name'] == p.name

    result = schema.execute(query('name_Exact:"' + p.name.upper() + '"'))
    assert result.data['person'] is None


def test_iexact(schema_builder, mock_person_filled):
    p = mock_person_filled()
    p.save()
    PersonSchema = MongraphSchema(mock_person_filled)

    schema = schema_builder([PersonSchema])

    result = schema.execute(query('name_Iexact:"' + p.name.lower() + '"'))
    assert result.data['person']['name'] == p.name

    result = schema.execute(query('name_Iexact:"' + p.name.upper() + '"'))
    assert result.data['person']['name'] == p.name


def test_contains(schema_builder, mock_person_filled):
    p = mock_person_filled()
    p.save()
    PersonSchema = MongraphSchema(mock_person_filled)

    schema = schema_builder([PersonSchema])

    result = schema.execute(query('name_Contains:"' + p.name[2:6] + '"'))
    assert result.data['person']['name'] == p.name

    result = schema.execute(query('name_Contains:"' + p.name[2:6].upper() + '"'))
    assert result.data['person'] is None


def test_icontains(schema_builder, mock_person_filled):
    p = mock_person_filled()
    p.save()
    PersonSchema = MongraphSchema(mock_person_filled)

    schema = schema_builder([PersonSchema])

    result = schema.execute(query('name_Icontains:"' + p.name[2:6].lower() + '"'))
    assert result.data['person']['name'] == p.name

    result = schema.execute(query('name_Icontains:"' + p.name[2:6].upper() + '"'))
    assert result.data['person']['name'] == p.name


def test_startswith(schema_builder, mock_person_filled):
    p = mock_person_filled()
    p.save()
    PersonSchema = MongraphSchema(mock_person_filled)

    schema = schema_builder([PersonSchema])

    result = schema.execute(query('name_Startswith:"' + p.name[0] + '"'))
    assert result.data['person']['name'] == p.name


def test_istartswith(schema_builder, mock_person_filled):
    p = mock_person_filled()
    p.save()
    PersonSchema = MongraphSchema(mock_person_filled)

    schema = schema_builder([PersonSchema])

    result = schema.execute(query('name_Istartswith:"' + p.name[0].upper() + '"'))
    assert result.data['person']['name'] == p.name


def test_endswith(schema_builder, mock_person_filled):
    p = mock_person_filled()
    p.save()
    PersonSchema = MongraphSchema(mock_person_filled)

    schema = schema_builder([PersonSchema])

    result = schema.execute(query('name_Endswith:"' + p.name[-1] + '"'))
    assert result.data['person']['name'] == p.name



def test_iendswith(schema_builder, mock_person_filled):
    p = mock_person_filled()
    p.save()
    PersonSchema = MongraphSchema(mock_person_filled)

    schema = schema_builder([PersonSchema])

    result = schema.execute(query('name_Iendswith:"' + p.name[-1].upper() + '"'))
    assert result.data['person']['name'] == p.name

