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
	user = graphene.Field(UserSchema, **UserSchema.fields, resolver=UserSchema.auto_resolver)
```
<br>

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
* EmailField
* LongField
* DecimalField
* BinaryField
* SortedListField
