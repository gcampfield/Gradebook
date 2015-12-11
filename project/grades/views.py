from flask import flash, redirect, render_template, request, url_for, Blueprint, jsonify
from flask.ext.login import login_required, current_user
from project.models import *

grades_blueprint = Blueprint(
    'grades', __name__,
    template_folder='templates'
)

@grades_blueprint.route('/')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@grades_blueprint.route('/<int:class_id>/')
@login_required
def class_view_id(class_id):
    my_class = Class.query.filter_by(user=current_user.id).filter_by(id=class_id).first()
    if my_class is None:
        flash('That class does not exist.')
        return redirect(url_for('grades.dashboard'))
    return render_template('class.html', class_=my_class)

@grades_blueprint.route('/new/grade/', methods=['POST'])
@login_required
def new_grade():
    category_arg = request.args.get('category', type=int)
    if category_arg is None:
        return jsonify(error='category must be an integer (id)')
    category = Grade_Category.query.filter_by(id=category_arg).first()
    if category is None:
        return jsonify(error='that category does not exist')

    owned_categories = []
    for class_ in current_user.classes:
        for cat in class_.categories:
            owned_categories.append(cat)

    if category not in owned_categories:
        return jsonify(error='user does not own this category')

    name = request.args.get('name', type=str)
    score = request.args.get('score', type=float)
    total = request.args.get('total', type=float)

    if score is None:
        return jsonify(error='must provide score field')
    if  total is None:
        return jsonify(error='must provide total field')

    grade = category.add_grade(score=score, total=total, name=name)

    return jsonify(error=None, grade=grade.serialize())

@grades_blueprint.route('/new/category/', methods=['POST'])
@login_required
def new_category():
    class_arg = request.args.get('class', type=int)
    if class_arg is None:
        return jsonify(error='class must be an integer (id)')
    class_ = Class.query.filter_by(id=class_arg).first()
    if class_ is None:
        return jsonify(error='that class does not exist')
    if class_ not in current_user.classes:
        return jsonify(error='user does not own this class')

    name = request.args.get('name', type=str)
    weight = request.args.get('weight', 1.0, type=float)
    points = request.args.get('points', 0.0, type=float)
    total = request.args.get('total', 0.0, type=float)

    if name is None:
        return jsonify(error='must provide name field')

    category = class_.add_category(name=name, weight=weight, points=points, total=total)

    return jsonify(error=None, category=category.serialize())

@grades_blueprint.route('/new/class/', methods=['POST'])
@login_required
def new_class():
    name = request.args.get('name', type=str)

    if name is None:
        return jsonify(error='must provide name field')

    class_ = current_user.add_class(name)

    return jsonify(error=None, class_=class_.serialize())
