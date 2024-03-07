import requests
import os
import pathos.multiprocessing as p
import pprint
from geocoding import Geocoder

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
        geo = Geocoder()
        # pp = pprint.PrettyPrinter(indent=4, width=80, compact=False)

        ''' To do: process start and end point and collect result as a dict??'''
        return None

# Checking if I manage to pull correctly:
# trying = EstTimePipeline()
# trying.process_data()

# print(os.environ.get("LTA_KEY"))
# data = trying.fetch_data()
# geo = Geocoder()
# pp = pprint.PrettyPrinter(indent=4, width=80, compact=False)
# pp.pprint(data)

# end = geo.getLocation(data['value'][0]['EndPoint'])

# print('\n')

# pp.pprint(data['value'][0])


# for i in data['value']:
#     print(i['EndPoint'])