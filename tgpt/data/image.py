import requests, os
import pathos.multiprocessing as p
import numpy as np
import geocoder
from PIL import Image

"""
This class pulls live traffic images from LTA cameras based on a latitude / longitude.
"""

class ImagePipeline:

    def __init__(self):
        self.url = "http://datamall2.mytransport.sg/ltaodataservice/Traffic-Imagesv2"
        self.headers = {'AccountKey' :  os.environ.get("LTA_KEY"), "accept" : "application/json"}
        self.n_core = p.cpu_count()//2

    def get_data_as_user(self):
        lat, long = self.get_user_lat_long()
        return self.get_data(lat, long)

    def get_user_lat_long(self):
        return geocoder.ip("me").latlng

    def get_data(self, lat, long):
        resp = requests.get(self.url, headers=self.headers).json()["value"]
        pool = p.ProcessingPool(nodes=self.n_core) 
        results = pool.amap(lambda x : self.process_camera_entry(x, lat, long), resp)
        pool.close()
        pool.join()
        pool.clear()
        results = min(results.get(), key=lambda x : x[0])
        im = Image.open(requests.get(results[1], stream=True).raw)
        return im
    
    def process_camera_entry(self, entry : dict, user_lat, user_long):
        camera_lat, camera_long = entry["Latitude"], entry["Longitude"]
        url = entry["ImageLink"]
        eucd = self.get_euclidean_dist(camera_lat, camera_long, user_lat, user_long)
        return (eucd, url)

    def get_euclidean_dist(self, lat_1, long_1, lat_2, long_2):
        return np.linalg.norm(np.subtract(np.array([lat_1, long_1]), np.array([lat_2, long_2])))
