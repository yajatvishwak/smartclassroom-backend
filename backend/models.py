from backend import db , ma
class Student(db.Model):
    sid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120),nullable=False)
    usn = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(80))
    classid = db.Column(db.String(30))
    def __repr__(self):
        return '<Student %r>' % self.username

class StudentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Student

    sid = ma.auto_field()
    username = ma.auto_field()
    password = ma.auto_field()
    usn = ma.auto_field()
    name = ma.auto_field()
    classid = ma.auto_field()

class Teacher(db.Model):
    tid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120),nullable=False)
    usn = db.Column(db.String(80), unique=True)
    name = db.Column(db.String(80))
    classHandled = db.Column(db.String(30)) # array stored in string
    def __repr__(self):
        return '<Teacher %r>' % self.username
class TeacherSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Teacher

    tid = ma.auto_field()
    username = ma.auto_field()
    password = ma.auto_field()
    usn = ma.auto_field()
    name = ma.auto_field()

class Notification(db.Model):
    nid= db.Column(db.Integer, primary_key=True)
    priority = db.Column(db.String(20),default="low")
    title = db.Column(db.String(120))
    desc = db.Column(db.String(256))
    classid = db.Column(db.String(30))
    tid = db.Column(db.Integer, db.ForeignKey("teacher.tid"))
class NotificationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Notification

    nid= ma.auto_field()
    priority = ma.auto_field()
    title = ma.auto_field()
    desc = ma.auto_field()
    classid = ma.auto_field()
    tid = ma.auto_field()


class SubmissionRequest(db.Model):
    srid = db.Column(db.Integer, primary_key=True)
    tid = db.Column(db.Integer, db.ForeignKey("teacher.tid"))
    title = db.Column(db.String(120))
    deadline = db.Column(db.String(100))
    desc = db.Column(db.String(256))
    classid = db.Column(db.String(100))

class SubmissionRequestSchema(ma.SQLAlchemySchema):
    class Meta:
        model = SubmissionRequest

    srid = ma.auto_field()
    tid = ma.auto_field()
    title = ma.auto_field()
    deadline = ma.auto_field()
    desc = ma.auto_field()
    classid = ma.auto_field()
    

class Submission(db.Model):
    subid = db.Column(db.Integer, primary_key=True)
    sid = db.Column(db.Integer , db.ForeignKey("student.sid"))
    srid = db.Column(db.Integer ,  db.ForeignKey("submission_request.srid"))
    filepath = db.Column(db.String(128))
    type = db.Column(db.String(10))
class SubmissionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Submission

    subid = ma.auto_field()
    sid = ma.auto_field()
    srid = ma.auto_field()
    filepath = ma.auto_field()
    type = ma.auto_field()
    

class Report(db.Model):
    rid = db.Column(db.Integer , primary_key =True)
    type = db.Column(db.String(30))
    total = db.Column(db.Integer)
    marksObtained = db.Column(db.Integer)
    sid = db.Column(db.Integer , db.ForeignKey("student.sid"))

class ReportSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Report

    rid = ma.auto_field()
    type = ma.auto_field()
    total = ma.auto_field()
    marksObtained = ma.auto_field()
    sid = ma.auto_field()