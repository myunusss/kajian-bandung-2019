from flask import Flask
from flask_restful import Api

from resources.kajian import Kajian, ListKajian
# from resources.kolaborasi import Kolaborasi
# from resources.iklan import Iklan
# from resources.quote import Quote

app = Flask(__name__)
api = Api(app)

# api.add_resource(Todo, "/todo/<int:id>")
api.add_resource(Kajian, "/kajian")
# api.add_resource(DetailKajian, "/kajian/detail")
# api.add_resource(ListKajian, "/list/kajian")
# api.add_resource(Kolaborasi, "/tim/kolaborasi")
# api.add_resource(Quote, "/quote")
# api.add_resource(Iklan, "/iklan")

if __name__ == "__main__":
  app.run()