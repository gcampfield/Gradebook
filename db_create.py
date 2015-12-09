from project import db
from project.models import User
db.create_all()
db.session.commit()
