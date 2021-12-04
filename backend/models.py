from backend import db
class Student(db.Model):
    sid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120),nullable=False)
    usn = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(80))
    classid = db.Column(db.String(30))
    reports = db.relationship("Report", backref="student")
    submissions = db.relationship("Submission" , backref="student")
    def __repr__(self):
        return '<Student %r>' % self.username
class Teacher(db.Model):
    tid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120),nullable=False)
    usn = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(80))
    notifications = db.relationship("Notification", backref="teacher")
    submissionRequests = db.relationship("SubmissionRequest", backref="teacher")
    classHandled = db.Column(db.String(30)) # array stored in string
    def __repr__(self):
        return '<Teacher %r>' % self.username
class Notification(db.Model):
    nid= db.Column(db.Integer, primary_key=True)
    priority = db.Column(db.String(20),default="low")
    title = db.Column(db.String(120))
    desc = db.Column(db.String(256))
    classid = db.Column(db.String(30))
    tid = db.Column(db.Integer, db.ForeignKey("teacher.tid"))


class SubmissionRequest(db.Model):
    srid = db.Column(db.Integer, primary_key=True)
    tid = db.Column(db.Integer, db.ForeignKey("teacher.tid"))
    title = db.Column(db.String(120))
    deadline = db.Column(db.String(100))
    desc = db.Column(db.String(256))
    submissions = db.relationship("Submission", backref="submissionrequest")
    

class Submission(db.Model):
    subid = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.Integer , db.ForeignKey("student.sid"))
    srid = db.Column(db.Integer ,  db.ForeignKey("submission_request.srid"))
    filepath = db.Column(db.String(128))
    type = db.Column(db.String(10)) 

class Report(db.Model):
    rid = db.Column(db.Integer , primary_key =True)
    type = db.Column(db.String(30))
    total = db.Column(db.Integer)
    marksObtained = db.Column(db.Integer)
    sid = db.Column(db.Integer , db.ForeignKey("student.sid"))