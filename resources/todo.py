from flask_restful import Resource

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
    # conn, cur = ConnectDB()
    # hasil = ""
    # try:
    #   cur.execute("select id_kajian, tanggal, deskripsi from kajian")
    #   hasil = "Berhasil"
    # except Exception as e:
    #   hasil = "Oopss"
    # finally:
    #   CloseDB(conn, cur)
    # return hasil
    for todo in todos:
      if(id == todo["id"]):
        return todo, 200
    return "Item not found for the id: {}".format(id), 404

    def put(self, id):
      for todo in todos:
        if(id == todo["id"]):
          todo["item"] = request.form["data"]
          todo["status"] = "Open"
          return todo, 200
      return "Item not found for the id: {}".format(id), 404