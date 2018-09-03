# project/example/views.py

from flask import render_template, Blueprint, request, flash, redirect, url_for
from .forms import Example_Form
from .example import PROJECT_data

example_blueprint = Blueprint('example', __name__, template_folder='templates')


@example_blueprint.route('/example', methods=['GET', 'POST'])
def example():
    example = Example_Form(request.form)
    if request.method == 'POST':
            flash('You POSTed something! YAY!!!', 'error')
    return render_template('example.html', form=example)
