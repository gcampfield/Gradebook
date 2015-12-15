from project import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String)

    def __init__(self, firstname, lastname, email, password):
        self.firstname = firstname
        self.lastname = lastname
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

    def add_class(self, name):
        class_ = Class(name, self)
        db.session.add(class_)
        db.session.commit()
        return class_

class Class(db.Model):
    __tablename__ = "classes"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    grade = db.Column(db.String, nullable=False)
    points = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship("User",
                        backref=db.backref('classes', lazy='dynamic'))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'grade': self.grade,
            'points': self.points,
            'total': self.total,
            'user_id': self.user_id,
            'categories': [category.serialize() for category in self.categories]
        }

    def __init__(self, name, user):
        self.name = name
        self.user = user
        self.points = 0
        self.total = 0
        self.grade = 'N/A'

    def update_grade(self):
        sum_weights = sum([cat.weight for cat in self.categories])
        points = 0
        total = 0
        for category in self.categories:
            if category.total > 0:
                points += category.points / category.total * category.weight
                total += category.weight
        self.points = points
        self.total = total
        if (total <= 0):
            self.grade = 'N/A'
        elif (points/total > .895):
            self.grade = 'A'
        elif (points/total > .795):
            self.grade = 'B'
        elif (points/total > .695):
            self.grade = 'C'
        elif (points/total > .595):
            self.grade = 'D'
        else:
            self.grade = 'F'

    def add_category(self, name, weight=1.0):
        category = Grade_Category(name, weight, self)
        db.session.add(category)
        db.session.commit()
        return category

    def delete(self):
        for category in self.categories:
            category.delete()
        db.session.delete(self)
        db.session.commit()

class Grade_Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    points = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    _class = relationship('Class',
                          backref=db.backref('categories', lazy='dynamic'))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'class_id': self.class_id,
            'weight': self.weight,
            'points': self.points,
            'total': self.total,
            'grades': [grade.serialize() for grade in self.grades]
        }

    def __init__(self, name, weight=1.0, class_=None):
        self.name = name
        self.weight = weight
        self.points = 0
        self.total = 0
        self._class = class_

    def add_grade(self, score, total, name=None):
        grade = Grade(name, score, total, self)
        self.points += score
        self.total += total
        self._class.update_grade()
        db.session.add(grade)
        db.session.commit()
        return grade

    def delete(self):
        class_ = self._class
        for grade in self.grades:
            grade.delete()
        db.session.delete(self)
        db.session.commit()
        class_.update_grade()
        return class_

class Grade(db.Model):
    __tablename__ = "grades"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    score = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = relationship('Grade_Category',
                            backref=db.backref('grades', lazy='dynamic'))

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'class_points': self.category._class.points,
            'class_total': self.category._class.total,
            'class_grade': self.category._class.grade,
            'category_id': self.category_id,
            'category_points': self.category.points,
            'category_total': self.category.total,
            'score': self.score,
            'total': self.total
        }

    def __init__(self, name, score, total, category):
        self.name = name
        self.score = score
        self.total = total
        self.category = category

    def delete(self):
        category = self.category
        self.category.points -= self.score
        self.category.total -= self.total
        self.category._class.update_grade()
        db.session.delete(self)
        db.session.commit()
        return category
