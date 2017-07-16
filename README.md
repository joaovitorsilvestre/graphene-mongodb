# GrapheneMongo

GrapheneMongo is a library that integrates <a href="https://github.com/graphql-python/graphene/" target="_blank">Graphene</a> with <a target="_blank" href="https://github.com/MongoEngine/mongoengine">MongoeEngine</a>
&nbsp; [![Build Status](https://travis-ci.org/joaovitorsilvestre/graphene-mongo.svg?branch=master)](https://travis-ci.org/joaovitorsilvestre/graphene-mongo)
[![Coverage Status](https://coveralls.io/repos/github/joaovitorsilvestre/graphene-mongo/badge.svg?branch=master)](https://coveralls.io/github/joaovitorsilvestre/graphene-mongo?branch=master)
<hr>

### Examples
Given that mongoengine Document:
```python
class User(Document):
    username = StringField()
    creation_date = DateTimeField()
    favourite_color = ListField(StringField())
```
To generage a graphene schema for that Document we create a class that is subclass of graphene_mongo.MongoSchema, or we can also just call it passing the model as first argument:
```python
from graphene_mongo import MongoSchema

class UserSchema(MongoSchema):
    model = User
# OR
UserSchema = MongoSchema(User)
```
The schema now it's generated. Now it's necessary to create a graphene object Query:
```python
import graphene

class Query(graphene.ObjectType):
    user = UserSchema.single
    
schema = graphene.Schema(query=Query)

# now we can do the query:
result = schema.execute("""
query Data {
    user(username: "John") {
		id
		username
    }
}""")
```

You may notice the UserSchema.single atribute in the example above, the class UserSchema has many other atrributes. All they are explained below:

| Atribute  | Description |
| ------------- | ------------- |
|  single  |  We use single we want that the query result be a unique result. That's the same that make the query in mongoengine calling .first() to get the first object that matchs the query.  |
| list  | List is used when we want a list of the documents that matchs the query. |
| model  | That's easy, this attribute stores the original Document of mongoengine that you created. |
| fields |  This field is more consult, you can use the fields that was converted from mongoengine to graphene. For instance, in our UserSchema class the attribute field will be a dict like this: {'username': graphene.String}|
| mutation | Mutate is the atribute that we use when creating Mutations with graphene. See more in [Mutations](#mutations) |

<br>

## Mutations

Somethimes we need to save new data in the mongodb instead of doing querys. Mutation that do that job.
Lets use again the <b>UserSchema</b> that we created in the examples. As before we created a graphene object called Query to handle the query, we now need to do the same to Mutation:

```python
class Mutation(graphene.ObjectType):
    create_user = UserSchema.mutate

schema = graphene.Schema(query=Query, mutation=Mutation)
```
Notice that we updated the variable schema to has the mutation object too.
Now we can do the mutation query and create a new user in our database:
```python
result = schema.execute("""
mutation testMutation {
  createPerson(username:"John") {
    person {
    	id
    	username
    }
  }
}""")
```

We pass pass the attributes that we want to save in the 'params', as wee did in "...createPerson(username:"John")..."

In this example graphene-mongo handled the save of the object to you, but somethimes you need to make validations before actualy save the object in to database. How you can do that is explain next.

### Verifications before save
To use your own function to save you need to create a function in the MongoSchema class called <b>mutate</b>. Said that, lets update our UserSchema as follows:
```python
class UserSchema(MongoSchema):
    model = User

    @staticmethod
    def mutate(args, context):
    	new_user = User(**args)
        new_user.creation_date = datetime.now()
        new_user.save()
        return new_user
```

There's not many rules here, you only need to be sure that the method receive two parameters, has the the staticmethod decorator and returns the instance of the object.

The <b>context</b> parameter has the request object of the framework that you're using. If you're using flask for instance, that parameter will be the <a href="http://werkzeug.pocoo.org/docs/0.12/local/#werkzeug.local.LocalProxy" target="_blank">flask global request</a>.



## Operators in query

Mongoengine offer many kinds of operators to use as 'in', 'gte', etc. See all operators in <a target="_blank" href="http://docs.mongoengine.org/guide/querying.html#query-operators">mongoengine documentation</a>. With Graphene-mongo you can use they in  your query:
```python
result = schema.execute("""
query Data {
    user(username_Icontains: "John", creationDate_Gte:"1997-04-28", favouriteColor_In:["red", "blue"]) {
		id
		username
    }
}""")
```

The best is that they are all supported by graphene-mongo.

<br>
<hr>
<br>


### TODOs
* Accept user mutation return None;
* Support ReferenceField of 'self' without raises 'maximum recursion' error.
