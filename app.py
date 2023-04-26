from flask import Flask, render_template
from resources import sql_queries, homepage
import static

# Create the application.
APP = Flask(__name__)


@APP.route('/')
def homepage():
    conn = sql_queries.connect_to_db()
    activities = sql_queries.get_activity_names(conn)
    return render_template('home_page.html', activities=activities)


if __name__ == '__main__':
    APP.debug=True
    APP.run()

@APP.route("/images/<name>")
def images(name):
    # fullpath = url_for('static', filename=name)
    return '<img src=' + Flask.url_for('static', filename='images/{}'.format(name)) + '>'