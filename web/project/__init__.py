import os
from flask import Flask, url_for, redirect
from project.example.views import example_blueprint
from flask_uploads import configure_uploads
from project.extensions import ddumps

app = Flask(__name__, instance_relative_config=True)
# app.config.from_pyfile('flask.cfg')

app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

app.register_blueprint(example_blueprint)

# re-route people to the atm login
@app.route('/')
def index():
    return redirect(url_for('example.example'))

configure_uploads(app, ddumps)


