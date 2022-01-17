from flask.scaffold import F
from backend import app
from flask.globals import request
from flask.json import jsonify
from backend.models import Notification, Report, Student, StudentSchema, Submission, SubmissionRequest, Teacher, TeacherSchema
from backend import db

from collections import defaultdict


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
         "teacherPicture":"https://via.placeholder.com/50",
         "type": i.type
          })
    return jsonify(res)

# teacher routes

@app.route("/loginTeacher", methods = ["POST"])
def loginTeacher():
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
        res.append({ "class": i.classid ,"title":i.title, "teacher": Teacher.query.filter_by(tid = i.tid).first().name , "priority": i.priority, "createdAt": "10.2.2" })
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
    type1  = request_data["type"]
    submissionRequest = SubmissionRequest(
        tid=tid,
        title=title,
        deadline=deadline,
        desc=desc,
        classid=targetClass,
        type=type1
    )
    db.session.add(submissionRequest)
    db.session.commit()
    return jsonify({"message": "added successfully" , "statuscode": 200, })

@app.route("/getAllStudents" , methods=["GET"])
def getAllStudents():
    # parameters required
    # class, priority, title, tid
    d= {}
    l = [studentSchema.dump(i) for i in Student.query.filter_by().all()]
    classes = []
    for i in l:
        classes.append(i["classid"])
    classes = list(set(classes))
    for i in classes:
        d[i] = []
    print(d)
    for i in l:
        print(d[i["classid"]])
        d[i["classid"]].append(i["usn"])
    return jsonify({"students": d, })

@app.route("/addEntry" , methods=["POST"])
def addEntry():
    request_data  = request.get_json()
    usn = request_data["usn"]
    sid = Student.query.filter_by(usn=usn).first().sid
    typeCategory = request_data["type"]
    total = request_data["total"]
    marksObtained = request_data["marksObtained"]
    rep = Report(sid=sid, type=typeCategory ,total=total ,marksObtained=marksObtained)
    db.session.add(rep)
    db.session.commit()
    return jsonify({"message": "added successfully" , "statuscode": 200, })


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
from werkzeug.utils import secure_filename
import os

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/turnin" , methods=["POST"])
def turnIn():
    sid = request.form["sid"]
    srid = request.form["srid"]
    subtype = request.form["type"]
    file = request.files['file']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    sub = Submission(sid = sid, srid = srid, type=subtype, filepath=filename)
    db.session.add(sub)
    db.session.commit()
    return jsonify({"message": "done"})
    
from flask import send_file
@app.route("/getfile" , methods=["POST"])
def getFile():
    request_data  = request.get_json()
    file = request_data["file"] 
    return send_file("D:\\vibhhhaa\\smartclassroom-backend\\uploads\\"+file)
    

@app.route("/getScores" , methods=["POST"])
def getScores():
    d={
        "assignments" : [],
        "cie": [],
        "quiz": []
    }
    request_data  = request.get_json()
    sid = request_data["sid"]
    ass1 = Report.query.filter_by(sid=sid, type="Assignment1").first()
    ass2 = Report.query.filter_by(sid=sid, type="Assignment2").first()
    quiz1 = Report.query.filter_by(sid=sid, type="Quiz1").first()
    quiz2 = Report.query.filter_by(sid=sid, type="Quiz2").first()
    cie1 = Report.query.filter_by(sid=sid, type="CIE1").first()
    cie2 = Report.query.filter_by(sid=sid, type="CIE2").first()
    cie3 = Report.query.filter_by(sid=sid, type="CIE3").first()

    if ass1 != None:
        d["assignments"].append( {"name": ass1.type, "total": ass1.total, "marks": ass1.marksObtained})
    if ass2 != None:
        d["assignments"].append( {"name": ass2.type, "total": ass2.total, "marks": ass2.marksObtained})
    if quiz1 != None:
        d["quiz"].append( {"name": quiz1.type, "total": quiz1.total, "marks": quiz1.marksObtained})
    if quiz2 != None:
        d["quiz"].append( {"name": quiz2.type, "total": quiz2.total, "marks": quiz2.marksObtained})

    if cie1 != None:
        d["cie"].append( {"name": cie1.type, "total": cie1.total, "marks": cie1.marksObtained})
    if cie2 != None:
        d["cie"].append( {"name": cie2.type, "total": cie2.total, "marks": cie2.marksObtained})
    if cie3 != None:
        d["cie"].append( {"name": cie3.type, "total": cie3.total, "marks": cie3.marksObtained})
    return jsonify(d)

    
    
    
    
    