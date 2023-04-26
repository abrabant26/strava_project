from flask import render_template
from resources import sql_queries


def activity_names():
    conn = sql_queries.connect_to_db()
    activities = sql_queries.get_activity_names(conn)
    print(activity_names)
    print(type(activity_names))
    template = render_template('home_page.html', activities=activities)
    return template