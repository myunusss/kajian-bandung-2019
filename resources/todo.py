from flask_restful import Resource
from dbconnect import ConnectDB, CloseDB

todos = [
  {
    "id": 1,
    "item": "Create sample app",
    "status": "Completed"
  },
  {
    "id": 2,
    "item": "Deploy in Heroku",
    "status": "Open"
  },
  {
    "id": 3,
    "item": "Publish",
    "status": "Open"
  }
]

class Todo(Resource):
  def get(self, id):
    conn, cur = ConnectDB()
    try:
      cur.execute("select id_kajian, tanggal, deskripsi from kajian")
      return "Berhasil"
    except Exception as e:
      return "Oopss"
    # for todo in todos:
    #   if(id == todo["id"]):
    #     return todo, 200
    # return "Item not found for the id: {}".format(id), 404

    def put(self, id):
      for todo in todos:
        if(id == todo["id"]):
          todo["item"] = request.form["data"]
          todo["status"] = "Open"
          return todo, 200
      return "Item not found for the id: {}".format(id), 404