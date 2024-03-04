import requests
import os
import pathos.multiprocessing as p

class TrafficFlowPipeline:
    def __init__(self):
        self.url = "http://datamall2.mytransport.sg/ltaodataservice/trafficflow"
        self.headers = {'AccountKey': os.environ.get("LTA_KEY"), "accept": "application/json"}
        self.n_core = p.cpu_count() // 2

    def get_traffic_data(self):
        response = requests.get(self.url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            return None