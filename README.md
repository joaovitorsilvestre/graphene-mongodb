# MongographQL
Implementation of Graphene and MongoEngine
<br>
<br>

## The proposal

Assume that you have the follow Document:

```python
class User(Document):
    name = StringField()
    age = IntField()
    favorite_colors = ListField(StringField())
```
To create a graphene schema for that document we can do:
```python
class UserSchema(graphene.ObjectType):
    name = graphene.String()
    age = graphene.Int() 
    favorite_colors = graphene.List(graphene.String)
    
class Query(graphene.ObjectType):
    user = graphene.Field(UserSchema, name=graphene.String(),
                                      age=graphene.Int(),
                                      favorite_colors=graphene.List(graphene.String))
    
    def resolve_user(self, args, context, info):
        ## It's necessary some bit of code to get 'args' and pass to 'User' query
        ## and return that as a dict with the results of each field 
        return UserSchema(**args)
```
Note that the example has a bit of 'duplicated' code in this example. 

The proposal of MongographQL is to make it cleaner and do all the work of query's and resolve things in background for you:

```python
class UserSchema(MongraphSchema):
    __MODEL__ = User
    
class Query(graphene.ObjectType):
    user = UserSchema.single()  # return the first that matchs the query
    users = UserSchema.list()   # return a list of the objects that matchs the query
```
<br>

## Flask example
```bash
cd ~/ && git clone https://github.com/joaovitorsilvestre/MongographQL.git && cd ~/MongographQL
mkvirtualenv MongographQL -p `which python3`
pip install -r requirements.txt && pip install -r dev-requirements.txt
export FLASK_APP=~/MongographQL/flask_example/__init__.py
flask run
```

Now is running on <a hfef="http://127.0.0.1:5000/graphql" target="_blank">http://127.0.0.1:5000/graphql</a>, try with this <a href="http://127.0.0.1:5000/graphql?query=query%20data%20%7B%0A%20%20user%20%7B%0A%20%20%09username%0A%20%20%20%20id%0A%20%20%20%20bank%20%7B%0A%20%20%20%20%20%20name%0A%20%20%20%20%7D%0A%20%20%7D%0A%20%20posts%20%7B%0A%20%20%20%20title%0A%20%20%7D%0A%7D&operationName=data" target="_blank">query</a>:
```
query data {
  user {
  	username
    id
    bank {
      name
    }
  }
  posts {
    title
  }
}
```

### Suported Fields
IntField, FloatField, StringField, BooleanField, ReferenceField, DateTimeField, LongField, ListField, ObjectId,        URLField, PointField, DictField, EmailField, DecimalField, BinaryField, SortedListField

### You can also use operators in query:
```
query data {
  user(username_Contains:"Joh") {
  	username
  }
  posts(title_In:["Post1", "Post2"]) {
    title
  }
}
```

### Suported Operators
in, nin, gte, lte, exact, iexact, contains, icontains, startswith, istartswith, endswith, iendswith


### Another examples
<a href="https://github.com/joaovitorsilvestre/MongographQL/blob/master/example.py" target="_blank">Simple example</a>
<br>
<a href="https://github.com/joaovitorsilvestre/MongographQL/blob/master/complex_example.py" target="_blank">Complex example</a>

## Run tests
``` bash
> py.test --cov MongographQL --verbose
> py.test --cov-report html --cov MongographQL --verbose
```
