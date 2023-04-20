from flask import Flask, request, jsonify
from flask_cors import CORS
from graphene import ObjectType, String, Schema, List, Mutation
from .api import db
from flask_graphql import GraphQLView


class Item(ObjectType):
    name = String()
    type = String()


class Query(ObjectType):
    users = List(Item)
    ttt = List(Item)

    def resolve_users(root, info):
        return [Item(
            name=x.get('name'),
            type=x.get('type')
        ) for x in db.data()]

    def resolve_ttt(root, info):
        return [Item(
            name=x.get('name'),
            type=x.get('type')
        ) for x in db.data()]


class CreateUser(Mutation):
    class Arguments:
        name = String(required=True)
        age = String(required=True)

    success = String()
    user = String()

    def mutate(self, info, name, age):
        # Code to create a new user in the database goes here
        # ...

        # db.put({'name': name, 'age': age})
        # print({'name': name, 'age': age})

        success = True
        user = f'User {name} created with age {age}'

        return CreateUser(success=success, user=user)


class Mutations(ObjectType):
    create_user = CreateUser.Field()


schema = Schema(query=Query, mutation=Mutations)


def create_app(config_file="config.py"):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    CORS(app)

    app.add_url_rule(
        '/graphql',
        view_func=GraphQLView.as_view(
            'graphql',
            schema=schema,
            graphiql=True
        ))

    # @app.post('/graphql')
    # def graphql():
    #     data = request.get_json()
    #     result = schema.execute(data['query'])
    #     print(type(result))
    #     print(dir(result))
    #     print(result.to_dict)
    #     return jsonify(result.data)

    return app
