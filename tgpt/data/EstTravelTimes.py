import requests
import os
import pathos.multiprocessing as p
import pprint
from geocoding import Geocoder
import re

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
    
    def process_data(self):
        data = self.fetch_data()
        return_data = []
        geo = Geocoder()
        pp = pprint.PrettyPrinter(indent=4, width=80, compact=False, sort_dicts=False)
        # pp.pprint(data)
        # print(len(data['value']))

        for loc in data['value']:
            start_loc = loc['StartPoint']
            end_loc = loc['EndPoint']
            if ("INTERCHANGE" in start_loc) or ("INTERCHANGE" in end_loc):
                continue
            geo.getLocationData(start_loc, end_loc, loc['EstTime'], return_data)
            # pp.pprint(return_data)

        pp.pprint(return_data)

        return None

# Checking if I manage to pull correctly:
get_data = EstTimePipeline()
get_data.process_data()


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