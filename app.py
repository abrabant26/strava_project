import flask
from resources import sql_queries
import static

# Create the application.
APP = flask.Flask(__name__)


@APP.route('/')
def homepage():
    """ Displays the index page accessible at '/'
    """
    return flask.render_template('home_page.html')


if __name__ == '__main__':
    APP.debug=True
    APP.run()

@APP.route("/images/<name>")
def images(name):
    # fullpath = url_for('static', filename=name)
    return '<img src=' + flask.url_for('static', filename='images/{}'.format(name)) + '>'