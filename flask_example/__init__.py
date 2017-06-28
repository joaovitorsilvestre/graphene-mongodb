from flask import Flask
from flask_graphql import GraphQLView
from mongoengine import connect
from .schema import schema, save_tests_in_db

connect('MongraphQL')

save_tests_in_db()

app = Flask(__name__)
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))


if __name__ == '__main__':
    app.run()