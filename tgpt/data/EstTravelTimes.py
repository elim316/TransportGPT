import requests
import os
import pathos.multiprocessing as p

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

# Checking if I manage to pull correctly:
print(os.environ.get("LTA_KEY"))
trying = EstTimePipeline()
data = trying.fetch_data()

for i in data['value']:
    print(i)

