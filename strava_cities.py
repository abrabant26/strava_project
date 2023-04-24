import requests
import urllib3
import polyline
from geopy.geocoders import Nominatim
import pandas as pd
import modules
from sqlalchemy import create_engine
import pymysql

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#get access token to hit strava api
def get_access_token():
    auth_url = "https://www.strava.com/oauth/token"
    payload = {
        'client_id': "105838",
        'client_secret': 'fbb8b018ccb46387dde4138e2e8633ce59bdd511',
        'refresh_token': '91796587e6ba99ddb2e4f87e875c15520cd786e5',
        'grant_type': "refresh_token",
        'f': 'json'
    }

    print("Requesting Token...\n")
    res = requests.post(auth_url, data=payload, verify=False)
    access_token = res.json()['access_token']
    print("Access Token = {}\n".format(access_token))
    return access_token

access_token = get_access_token()

#pull my athlete data
def get_data(access_token, per_page=100, page=1):
    activity_url = "https://www.strava.com/api/v3/athlete/activities"
    header = {'Authorization': 'Bearer ' + access_token}
    param = {'per_page': per_page, 'page': page}
    my_dataset = requests.get(activity_url, headers=header, params=param).json()
    
    print("finished pulling the data")
    return my_dataset

data = get_data(access_token)

#get existing activty ids from db and filter them for only new activities in the api call

# explode polyline map into coordinates and get towns/cities and states passed through for each exercise
def add_coordinates(data):
    # Initialize Nominatim API
    geolocator = Nominatim(user_agent="MyApp")
    outside_activities = []
    for activity in data:
        if(activity["map"]["summary_polyline"] != ''):
            coordinates = polyline.decode(activity["map"]["summary_polyline"])
            activity["map_coordinates"] = coordinates
            town_cities = []
            states = []
            for coordinate in activity['map_coordinates']:
                coordinate_pair = coordinate
                location = geolocator.reverse(coordinate_pair)
                address = location.raw['address']
                #print(address)
                if 'city' in address:
                    town_city = address['city']
                if 'town' in address:
                    town_city = address['town']
                if 'suburb' in address:
                    town_city = address['suburb']
                state = location.raw['address']['state']
                if town_city not in town_cities:
                    town_cities.append(town_city)
                if state not in states:
                    states.append(state)
            activity["town_cities"] = town_cities 
            activity["states"] = states
            outside_activities.append(activity)
    print(outside_activities[0]["map_coordinates"][0])
    print(outside_activities[0]["name"])
    print("got coordinates!")
    return outside_activities

outside_activities = add_coordinates(data)

def prepare_output(outside_activities):
    all_activities = []
    for activity in outside_activities:
        activity_data = {}
        activity_data['activity_id']= activity['id']
        activity_data['name'] = activity['name']
        activity_data['date'] = activity['start_date_local']
        activity_data['distance'] = activity['distance']
        activity_data['moving_time'] = activity['moving_time']
        activity_data['towns_cities_crossed'] = activity['town_cities']
        activity_data['num_towns_cities'] = len(activity['town_cities'])
        activity_data['states_crossed'] = activity['states']
        activity_data['num_states'] = len(activity['states'])
        all_activities.append(activity_data)
    all_activities = pd.DataFrame.from_dict(all_activities)
    all_activities['date'] = pd.to_datetime(all_activities['date'])
    activity_datatypes = {
        "activity_id":int,
        "distance":float,
        "moving_time":float,
        "towns_cities_crossed":str,
        "num_towns_cities":int,
        "states_crossed":str,
        "num_states":int
    }

    all_activities = all_activities.astype(activity_datatypes)
    all_activities.info()
    print(all_activities)
    print("done formating data!")

    return all_activities

activities = prepare_output(outside_activities)

def insert_data(activities):

    engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                       .format(user="abrabant26",
                               pw="Hermione26!",
                               host="ab-strava-data.cluster-cxs9osnnrcdx.us-east-1.rds.amazonaws.com",
                               db="sys"))
    # Insert whole DataFrame into MySQL
    activities.to_sql('activities', con = engine, if_exists = 'append', index=False, chunksize = 1000)
    print("data inserted! woo!")

insert_data(activities)