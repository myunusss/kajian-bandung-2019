from flask import Flask
from flask_restful import Api
from flask.ext.sqlalchemy import SQLAlchemy

from resources.todo import Todo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)
api = Api(app)

api.add_resource(Todo, "/todo/<int:id>")

if __name__ == "__main__":
  app.run()