from flask import Flask, render_template
from pages import homepage
from resources import sql_queries
import static

# Create the application.
APP = Flask(__name__)


@APP.route('/')
def home_page():
    activities = homepage.activity_names()
    return render_template('home_page.html', activities=activities)


if __name__ == '__main__':
    APP.debug=True
    APP.run()

@APP.route("/images/<name>")
def images(name):
    # fullpath = url_for('static', filename=name)
    return '<img src=' + Flask.url_for('static', filename='images/{}'.format(name)) + '>'