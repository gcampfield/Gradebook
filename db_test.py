from project.models import *
from project.users.views import new_user

grant = User.query.first()
if grant is None or grant.email != "grant@gcampfield.com":
    grant = new_user("Grant Campfield", "grant@gcampfield.com", "password")
db.session.add(grant)
db.session.commit()

concepts = Class("21-127", grant)
db.session.add(concepts)
db.session.commit()

tests = Grade_Category("Tests", concepts, 1.0)
db.session.add(tests)
db.session.commit()
tests.add_grade(45, 50, "Midterm 1")
tests.add_grade(48, 50, "Midterm 2")
tests.add_grade(43, 50, "Midterm 3")

homeworks = Grade_Category("Homework", concepts, 1.0)
db.session.add(homeworks)
db.session.commit()
homeworks.add_grade(35.0, 35)
homeworks.add_grade(34.0, 35)
homeworks.add_grade(32.5, 35)
homeworks.add_grade(35.0, 35)
homeworks.add_grade(35.0, 35)
homeworks.add_grade(34.5, 35)
homeworks.add_grade(28.0, 35)
