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
def classview(class_id):
    my_class = Class.query.filter_by(user=current_user).filter_by(id=class_id).first()
    if my_class is None:
        flash('That class does not exist.')
        return redirect(url_for('grades.dashboard'))
    return render_template('class.html', class_=my_class)

@grades_blueprint.route('/new/grade/', methods=['POST'])
@login_required
def new_grade():
    category_arg = request.values.get('category', type=int)
    if category_arg is None:
        return jsonify(error='must provide category field (int)')
    category = Grade_Category.query.filter_by(id=category_arg).first()
    if category is None:
        return jsonify(error='that category does not exist')

    owned_categories = []
    for class_ in current_user.classes:
        for cat in class_.categories:
            owned_categories.append(cat)

    if category not in owned_categories:
        return jsonify(error='user does not own this category')

    name = request.values.get('name', type=str)
    score = request.values.get('score', type=float)
    total = request.values.get('total', type=float)

    if score is None:
        return jsonify(error='must provide score field')
    if  total is None:
        return jsonify(error='must provide total field')

    grade = category.add_grade(score=score, total=total, name=name)

    return jsonify(error=None, grade=grade.serialize())

@grades_blueprint.route('/new/category/', methods=['POST'])
@login_required
def new_category():
    class_arg = request.values.get('class', type=int)
    if class_arg is None:
        return jsonify(error='must provide class field (int)')
    class_ = Class.query.filter_by(id=class_arg).first()
    if class_ is None:
        return jsonify(error='that class does not exist')
    if class_ not in current_user.classes:
        return jsonify(error='user does not own this class')

    name = request.values.get('name', type=str)
    weight = request.values.get('weight', 1.0, type=float)

    if name is None or name == "":
        return jsonify(error='must provide name field')

    category = class_.add_category(name=name, weight=weight)

    return jsonify(error=None, category=category.serialize())

@grades_blueprint.route('/new/class/', methods=['POST'])
@login_required
def new_class():
    name = request.values.get('name', type=str)

    if name is None or name == "":
        return jsonify(error='must provide name field')

    class_ = current_user.add_class(name)

    return jsonify(error=None, class_=class_.serialize())

@grades_blueprint.route('/delete/grade/', methods=['POST'])
@login_required
def delete_grade():
    return jsonify(error='feature not implemented yet')

@grades_blueprint.route('/delete/category/', methods=['POST'])
@login_required
def delete_category():
    return jsonify(error='feature not implemented yet')

@grades_blueprint.route('/delete/class/', methods=['POST'])
@login_required
def delete_class():
    return jsonify(error='feature not implemented yet')
