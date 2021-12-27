from backend import db

from backend.models import Student, Report

# vibha =  Student(sid=1, username="vibha", password="vibha", usn="1nh19cs196", name="vibha", classid="5d")
# yoyo =  Student(sid=2, username="bro", password="vibha", usn="1nh19cs192", name="bro", classid="5d")

# db.session.add_all([vibha,yoyo])
# db.session.commit()

# vibhasReport = Report(rid=1 , type="assignment", total=10, marksObtained=10, sid=1)
# db.session.add(vibhasReport)
# db.session.commit()

vibha = Student.query.filter_by(username="vibha").first()
print(vibha.reports[0].total)