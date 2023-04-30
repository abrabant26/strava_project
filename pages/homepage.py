from flask import render_template
from resources import sql_queries
import re


def activity_names():
    conn = sql_queries.connect_to_db()
    activities = sql_queries.get_activity_names(conn)
    activity_clean = []
    for activity in activities:
        #convert date and distance
        date = activity[1].strftime("%a %B %d, %Y")
        distance_mi = round(activity[2] * 0.000621371192, 2)

        #clean activity type
        activity_type = activity[3]
        if activity_type == 'Bike' or activity_type =='Ride':
            activity_type = 'biked'
        elif activity_type == 'Run':
            activity_type = 'ran'
        elif activity_type == 'Hike':
            activity_type = 'hiked'
        elif activity_type == 'Walk':
            activity_type = 'walked'
        else:
            activity_type = 'traveled'        

        #clean city list for printing
        city_list = activity[4].split(",")
        pattern = r"[^\w\s]"

        #create sentence from cities crossed
        i = 0
        list_len = len(city_list)
        cities_clean = []
        for city in city_list:
            city = re.sub(pattern,'',city)
            city = city.strip(" '")
            if i != list_len - 1 and i != 0 and list_len > 1:
                city_to_append = ", " + city
                cities_clean.append(city_to_append)
            if i == list_len - 1 and list_len > 2:
                grammer = ", and " + city
                cities_clean.append(grammer)
            if i == list_len - 1 and list_len == 2:
                grammer = " and " + city
                cities_clean.append(grammer)    
            if list_len == 1 or i == 0:
                cities_clean.append(city)
            i = i + 1
        city_sentence = ''.join(cities_clean)

        #clean state list
        state_list = activity[6].split(",")
        i = 0
        list_len = len(state_list)
        states_clean = []
        for state in state_list:
            state = re.sub(pattern,'',state)
            state = state.strip(" '")
            if i != list_len - 1 and i != 0 and list_len > 1:
                state_to_append = ", " + state
                states_clean.append(state_to_append)
            elif i == list_len - 1 and list_len > 2:
                grammer = ", and " + state
                states_clean.append(grammer)
            elif i == list_len - 1 and list_len == 2:
                grammer = " and " + state
                states_clean.append(grammer)  
            elif list_len == 1 or i == 0:
                states_clean.append(state)
            i = i + 1
        state_sentence = ''.join(states_clean)

        #create activity description
        base_description = "On " + str(date) + ", I " + activity_type + " " + str(distance_mi) + " miles, crossing " + str(activity[5])
        if activity[5] > 1:
            base_description = base_description + " towns (" + city_sentence + ")"
        if activity[5] == 1:
            base_description = base_description + " town (" + city_sentence + ")"
        if activity[7] > 1:
            base_description = base_description + " and " + str(activity[7]) + " states (" + state_sentence + ")."
        if activity[7] == 1:
            base_description = base_description + "."    
    

        activity_clean.append({
            "name": activity[0],
            "date": date,
            "distance": distance_mi,
            "towns_cities_crossed": city_sentence,
            "num_towns_cities": activity[5],
            "states_crossed": state_sentence,
            "num_states": activity[7],
            "activity_description": base_description
        })
    # template = render_template('home_page.html', activities=activity_clean)
    # return template
    return activity_clean

activity_names()