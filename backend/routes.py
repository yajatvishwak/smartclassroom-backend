from backend import app
from flask.globals import request
from flask.json import jsonify
from backend.models import Notification, Student, StudentSchema, Submission, SubmissionRequest, Teacher, TeacherSchema
from backend import db


studentSchema = StudentSchema()
teacherSchema = TeacherSchema()

@app.route("/") 
def hello():
    return "This is server page. This means the server is online and ready for smart classroom"

@app.route("/loginStudent", methods = ["POST"])
def loginStudent():
    request_data = request.get_json()
    username = request_data["username"]
    password =  request_data["password"]
    user = Student.query.filter_by(username=username).first()
    print(user)
    if not user == None and user.password == password:
        return jsonify({"message": "auth successful", "user": studentSchema.dump(user) })
    else:
        return jsonify({"message": "auth unsuccessful"})

@app.route("/loginTeacher", methods=["POST"])
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


# student routes
@app.route("/getNotification" , methods=["POST"])
def getNotification():
    # parameters required
    # class of the student 
    request_data  = request.get_json()
    classOfStudent = request_data["class"]
    allNotification = Notification.query.filter_by(classid = classOfStudent).all()
    print(allNotification)
    res = []
    for i in allNotification:
        res.append({"title":i.title, "teacher": Teacher.query.filter_by(tid = i.tid).first().name , "priority": i.priority })
    return jsonify(res)



@app.route("/getSubmissionRequest" , methods=["POST"])
def getSubmissionRequest():
    # parameters required
    # class of the student 
    request_data  = request.get_json()
    classOfStudent = request_data["class"]
    allSubmissionRequest = SubmissionRequest.query.filter_by(classid = classOfStudent).all()
    #print(allSubmissionRequest)
    res = []
    for i in allSubmissionRequest:
        res.append({"title":i.title,
         "assignedTeacher": Teacher.query.filter_by(tid = i.tid).first().name , 
         "deadline": i.deadline,
         "description" : i.desc,
         "submissionID" : i.srid,
         "teacherPicture":"https://via.placeholder.com/50"
          })
    return jsonify(res)

# teacher routes

@app.route("/loginTeacher", methods = ["POST"])
def loginStudent():
    request_data = request.get_json()
    username = request_data["username"]
    password =  request_data["password"]
    user = Teacher.query.filter_by(username=username).first()
    print(user)
    if not user == None and user.password == password:
        return jsonify({"message": "auth successful", "user": teacherSchema.dump(user) })
    else:
        return jsonify({"message": "auth unsuccessful"})

@app.route("/getTeacherSubmissionDetails" , methods=["POST"])
def getTeacherSubmissionDetails():
    # parameters required
    # srid  
    request_data  = request.get_json()
    srid = request_data["srid"]
    allSubmission = Submission.query.filter_by(srid=srid).all()
    res = []
    for i in allSubmission:
        res.append({
         "studentName": Student.query.filter_by(sid = i.sid).first().name , 
         "studentUSN": Student.query.filter_by(sid = i.sid).first().usn ,
         "class": Student.query.filter_by(sid = i.sid).first().classid ,
         "deadline": SubmissionRequest.query.filter_by(srid= i.srid).first().deadline,
         "filepath" : i.filepath
          })
    return jsonify(res)


@app.route("/getTeacherSubmissionRequest" , methods=["POST"])
def getTeacherSubmissionRequest():
    # parameters required
    # tid
    request_data  = request.get_json()
    tid = request_data["tid"]
    allSubmissionRequest = SubmissionRequest.query.filter_by(tid = tid).all()
    res = []
    for i in allSubmissionRequest:
        res.append({"title":i.title,
         "teacher": Teacher.query.filter_by(tid = i.tid).first().name , 
         "deadline": i.deadline,
         "desc" : i.desc,
         "class": i.classid,
         "srid": i.srid
          })
    return jsonify(res)

@app.route("/getTeacherNotification" , methods=["POST"])
def getTeacherNotification():
    # parameters required
    # tid 
    request_data  = request.get_json()
    tid = request_data["tid"]
    allNotification = Notification.query.filter_by(tid= tid).all()
    print(allNotification)
    res = []
    for i in allNotification:
        res.append({"title":i.title, "teacher": Teacher.query.filter_by(tid = i.tid).first().name , "priority": i.priority, "createdAt": "10.2.2" })
    return jsonify(res)



@app.route("/createNotification" , methods=["POST"])
def createNotification():
    # parameters required
    # class, priority, title, tid
    request_data  = request.get_json()
    targetClass = request_data["class"]
    tid = request_data["tid"]
    priority = request_data["priority"]
    title = request_data["title"]
    notification = Notification(priority=priority, tid=tid, title=title, classid=targetClass)
    teacher = Teacher.query.filter_by(tid = tid).first()
    db.session.add(notification)
    db.session.commit()
    return jsonify({"message": "added successfully" , "statuscode": 200, "insertedNotification": notification.nid, "teacher": teacher.name})

@app.route("/createSubmissionRequest" , methods=["POST"])
def createSubmissionRequest():
    # parameters required
    # class, priority, title, tid
    request_data  = request.get_json()
    targetClass = request_data["class"]
    tid = request_data["tid"]
    desc = request_data["desc"]
    deadline = request_data["deadline"]
    title = request_data["title"]
    submissionRequest = SubmissionRequest(
        tid=tid,
        title=title,
        deadline=deadline,
        desc=desc,
        classid=targetClass
    )
    db.session.add(submissionRequest)
    db.session.commit()
    return jsonify({"message": "added successfully" , "statuscode": 200, })
