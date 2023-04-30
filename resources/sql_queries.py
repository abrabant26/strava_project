import pymysql

#sql credentials
HOST = "ab-strava-data.cluster-cxs9osnnrcdx.us-east-1.rds.amazonaws.com"
USER = "abrabant26"
PASSWORD = "Hermione26!"
DATABASE = "sys"

#database connection
def connect_to_db():
    connection = pymysql.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )
    return connection

conn = connect_to_db()

#get activities in table so we don't import again
def get_existing_activites(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT activity_id FROM sys.activities")
    return cursor

def get_activity_names(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name, date, distance, activity_type, towns_cities_crossed, num_towns_cities, states_crossed, num_states FROM sys.activities")
    activity_name = []
    for activity in cursor:
        activity_name.append(activity)
    return activity_name

get_activity_names(conn)