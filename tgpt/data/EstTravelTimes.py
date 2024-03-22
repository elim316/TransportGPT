import requests
import os
import pathos.multiprocessing as p
import pprint
from geocoding import Geocoder
import re
import numpy as np
from sklearn.neighbors import NearestNeighbors
import numpy as np
from sklearn.neighbors import NearestNeighbors
from geocoding import distance

class EstTimePipeline:

    def __init__(self):
        self.url = "http://datamall2.mytransport.sg/ltaodataservice/EstTravelTimes"
        self.headers = {'AccountKey' : os.environ.get("LTA_KEY"), "accept": "application/json"} 
        # for the header what should accept be, its also application/json right?

    def fetch_data(self):
        try:
            resp = requests.get(self.url, headers=self.headers)
            resp.raise_for_status()
            print("success")
            return resp.json()
        except requests.RequestException as e:
            print(f"Error fetching data: {e}")
            return None
    
    def knn_model(self, trafficData, user):
        route = np.array([[float(i['start_lat']), 
                          float(i['start_lon']),
                          float(i['end_lat']),
                          float(i['end_lon'])] for i in trafficData])
        knn = NearestNeighbors(n_neighbors=len(route))
        knn.fit(route)

        userlocation = np.array([[user[0], user[1], user[2], user[3]]])
        distances, indices = knn.kneighbors(userlocation)

        closest_route = trafficData[indices[0][0]]
        user_dist = distance.distance((user[0], user[1]), (user[2], user[3])).km   
        # print(user_dist)
        # print(closest_route['dist'])
        
        # factor = user_dist/float(closest_route['dist'])
        # print(factor)
        return (closest_route['est_time'])


    def process_data(self, user):
        data = self.fetch_data()
        return_data = []
        geo = Geocoder()
        pp = pprint.PrettyPrinter(indent=4, width=80, compact=False, sort_dicts=False)

        for loc in data['value']:
            start_loc = loc['StartPoint']
            end_loc = loc['EndPoint']
            if ("INTERCHANGE" in start_loc) or ("INTERCHANGE" in end_loc):
                continue
            geo.getLocationData(start_loc, end_loc, loc['EstTime'], return_data)
            # pp.pprint(return_data)

        # pp.pprint(return_data) 
        estTime = self.knn_model(return_data, user)
        print(estTime)
        return estTime

# Checking if I manage to pull correctly:
get_data = EstTimePipeline()
print(get_data.process_data([1.3272336, 104,1.3117715, 102]))


# print(os.environ.get("LTA_KEY"))
# data = get_data.fetch_data()

# geo = Geocoder()
# pp = pprint.PrettyPrinter(indent=4, width=80, compact=False)
# pp.pprint(data)

# print(len(data['value']))


# for loc in data['value']:
#     start_loc = loc['StartPoint']
#     end_loc = loc['EndPoint']
#     if ("INTERCHANGE" in start_loc) or ("INTERCHANGE" in end_loc):
#         continue
#     est_time = loc['EstTime']
#     geo.getLocationData(loc['StartPoint'], loc['EndPoint'], loc['EstTime'])


# print("\n \n")
# print(data['value'][50]['StartPoint'])

# end.type()
# print(end)

# pp.pprint(data['value'][0])


# for i in data['value']:
#     print(i['EndPoint'])