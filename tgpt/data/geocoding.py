from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from geopy import distance
import re
import json
import pprint


class Geocoder:

    def getLocationData(cls, start_loc, end_loc, est_time, return_data):
        
        pp = pprint.PrettyPrinter(indent=4, width=80, compact=False)
        geolocator = Nominatim(user_agent="geolocator")

        start = geolocator.geocode(start_loc+", Singapore")
        end = geolocator.geocode(end_loc+", Singapore")

        if not start or not end:
            return None
        
        start_name = start.raw["display_name"]
        start_lat = float(start.raw["lat"])
        start_lon = float(start.raw["lon"])
        end_name = end.raw["display_name"]
        end_lat = end.raw["lat"]
        end_lon = end.raw["lon"]
        geo_dist = distance.distance((start_lat, start_lon), (end_lat, end_lon)).km
        # print(geo_dist)


        return_data.append({'start_name': start_name,
                            'start_lat': start_lat,
                            'start_lon' : start_lon,
                            'end_name': end_name,
                            'end_lat': end_lat,
                            'end_lon': end_lon,
                            'dist': geo_dist,
                            'est_time': est_time
                            })
        return None

    # def getLatandLon(cls):
