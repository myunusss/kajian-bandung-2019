from flask import Flask
from flask_restful import Api

from resources.kajian import Kajian, ListKajian, DetailKajian, Resume
from resources.kolaborasi import Kolaborasi
from resources.iklan import Iklan, NewInfo
from resources.quote import QuoteToday, AllQuote
from resources.manage import AddKajian, AddPemateri, AllIklan, AllKolaborasi, AllPemateri

app = Flask(__name__)
api = Api(app)

# api.add_resource(Todo, "/todo/<int:id>")
api.add_resource(Kajian, "/kajian")
api.add_resource(ListKajian, "/list/kajian")
api.add_resource(DetailKajian, "/detail/kajian")
api.add_resource(Resume, "/resume/kajian")
api.add_resource(Kolaborasi, "/tim/kolaborasi")
api.add_resource(QuoteToday, "/today/quote")
api.add_resource(AllQuote, "/quote")
api.add_resource(Iklan, "/iklan")
api.add_resource(AddKajian, "/tambah/kajian")
api.add_resource(AddPemateri, "/tambah/pemateri")
api.add_resource(AllIklan, "/all/iklan")
api.add_resource(AllKolaborasi, "/all/kolaborasi")
api.add_resource(AllPemateri, "/all/pemateri")
api.add_resource(NewInfo, "/new_info")

if __name__ == "__main__":
  app.run()