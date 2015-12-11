from project import db
db.drop_all()
db.session.commit()
