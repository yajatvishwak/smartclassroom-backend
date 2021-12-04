from backend import app
from flask.globals import request
from flask.json import jsonify
from backend.models import Student, Teacher

@app.route("/")
def hello():
    return "This is server page. This means the server is online and ready for smart classroom"

@app.route("/loginStudent")
def loginStudent():
    request_data = request.get_json()
    username = request_data["username"]
    password =  request_data["password"]
    user = Student.query.filter_by(username=username).first()
    print(user) 
   # return jsonify(True)

    if not user == None and user.password == password:
        return jsonify({"message": "auth successful"})
    else:
        return jsonify({"message": "auth unsuccessful"})

@app.route("/loginTeacher")
def loginTeacher():
    request_data = request.get_json()
    username = request_data["username"]
    password =  request_data["password"]
    user = Teacher.query.filter_by(username=username).first()
    print(user) 
   # return jsonify(True)

    if not user == None and user.password == password:
        return jsonify({"message": "auth successful"})
    else:
        return jsonify({"message": "auth unsuccessful"})