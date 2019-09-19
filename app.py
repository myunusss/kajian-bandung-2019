from flask import Flask
from flask_restful import Api

from resources.kajian import Kajian, ListKajian
from resources.kolaborasi import Kolaborasi

app = Flask(__name__)
api = Api(app)

# api.add_resource(Todo, "/todo/<int:id>")
api.add_resource(Kajian, "/kajian")
api.add_resource(Kolaborasi, "/tim/kolaborasi")
api.add_resource(ListKajian, "/list/kajian")

if __name__ == "__main__":
  app.run()