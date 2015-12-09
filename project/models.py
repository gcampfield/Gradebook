from project import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String)
    classes = relationship("Class")

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

class Class(db.Model):
    __tablename__ = "classes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    user = db.Column(db.Integer, ForeignKey('users.id'))
    categories = relationship("Grade_Category")

    def __init__(self, name, user):
        self.name = name
        self.user = user.id

class Grade_Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    _class = db.Column(db.Integer, ForeignKey('classes.id'))
    weight = db.Column(db.Float)
    points = db.Column(db.Integer)
    total = db.Column(db.Integer)
    grades = relationship("Grade")

    def __init__(self, name, _class, weight, points=0, total=0):
        self.name = name
        self._class = _class.id
        self.weight = weight
        self.points = points
        self.total = total

    def add_grade(self, score, total, name=None):
        grade = Grade(name, self, score, total)
        db.session.add(grade)
        self.points += score
        self.total += total
        db.session.add(self)
        db.session.commit()

class Grade(db.Model):
    __tablename__ = "grades"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    category = db.Column(db.Integer, ForeignKey('categories.id'))
    score = db.Column(db.Float)
    total = db.Column(db.Float)

    def __init__(self, name, category, score, total):
        self.name = name
        self.category = category.id
        self.score = score
        self.total = total
