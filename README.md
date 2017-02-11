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

The proprosal of MongographQL is to make it cleaner and do all the work of query's and resolve things in background for you:

```python
class UserSchema(metaclass=MongraphSchema):
    __MODEL__ = User
    
class Query(graphene.ObjectType):
	user = graphene.Field(UserSchema, **UserSchema.fields, resolver=UserSchema.auto_resolver)
```
<br>

MongographQL has suport for ReferenceField, and to use it you'll need to has already created the schema of the referenced document to MongraphSchema know how handle it:
```python
class User(Document):   
    name = StringField()

class Post(Document):
    author = ReferenceField(User)
    title = StringField()
    body = StringField()
       
class UserSchema(metaclass=MongraphSchema):
    __MODEL__ = User

class SchemaPost(metaclass=MongraphSchema):
    __MODEL__ = Post
    __REF__ = {'author': UserSchema}
```
### Examples
<a href="https://github.com/joaovitorsilvestre/MongographQL/blob/master/example.py" >Simple example</a>
<br>
<a href="https://github.com/joaovitorsilvestre/MongographQL/blob/master/complexExample.py" >Complex example</a>

### Suported Fields
* IntField
* FloatField
* StringField
* BooleanField
* ReferenceField
* DateTimeField
* ListField 
* ObjectId
* URLField
* PointField
* DictField
