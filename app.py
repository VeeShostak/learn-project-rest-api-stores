import os# postgres://okdcrciecnwvrm:74f9521e77d7a4e9003c4eb5f01e3de458b479b0d97f513351729e81b66f0f51@ec2-54-235-210-115.compute-1.amazonaws.com:5432/dbsi51cf36roti

from flask import Flask
from flask_restful import Api

from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList # SQLAlchemy only creates tables that it sees

app = Flask(__name__)
#SQLAlchemy db will be in root folder of our project (can by MySQL, PostgreSql, oracle...etc)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# in heroku get env db var, if not found, use our sqlite for testing in our local env
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
# FlaskSqlAlchemy know when object changed but not have saved to the db = turn off
# SQLAlchemy main library itself has a modification tracker
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'werete'
api = Api(app)

# SqlAlchemy can create db for us
# Use flask decorator 
# before first request run: app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' unless it alread exists
# @app.before_first_request
# def create_tables():
#     db.create_all() # only creates tables that it sees

jwt = JWT(app, authenticate, identity)  # /auth

api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
	# avoid Circular imports
	# Our item and models, import db as well.
	# If we import db at top, and import models at top, we have a circular import
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
