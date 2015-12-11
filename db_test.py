from project.models import *
from project.users.views import new_user

grant = User.query.filter_by(email="grant@gcampfield.com").first()
if grant is None:
    grant = new_user("Grant", "Campfield", "grant@gcampfield.com", "password")
db.session.add(grant)
db.session.commit()

concepts = grant.add_class("21-127")

tests = concepts.add_category("Tests")
tests.add_grade(45, 50, "Midterm 1")
tests.add_grade(48, 50, "Midterm 2")
tests.add_grade(43, 50, "Midterm 3")

homeworks = concepts.add_category("Homework")
homeworks.add_grade(35.0, 35)
homeworks.add_grade(34.0, 35)
homeworks.add_grade(32.5, 35)
homeworks.add_grade(35.0, 35)
homeworks.add_grade(35.0, 35)
homeworks.add_grade(34.5, 35)
homeworks.add_grade(28.0, 35)
