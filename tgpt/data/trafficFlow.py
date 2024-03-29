import requests
import os
import pathos.multiprocessing as p
import numpy as np
import geocoder
import pprint
import pandas as pd
import json
from sklearn.neighbors import KNeighborsRegressor
from sklearn import model_selection
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score

class TrafficFlowPipeline:
    def __init__(self):
        self.url = "http://datamall2.mytransport.sg/ltaodataservice/TrafficFlow"
        self.headers = {'AccountKey': os.environ.get("LTA_KEY"), "accept": "application/json"}
        # self.n_core = p.cpu_count() // 2

    def get_traffic_data_as_user(self):
        lat, long = self.get_user_lat_long()
        return self.get_traffic_data(lat, long)

    def get_user_lat_long(self):
        user_location = geocoder.ip("me")
        if user_location.ok:
            return user_location.latlng
        else:
            print("Failed to retrieve user's location.")
            return None

    def get_traffic_data(self, lat, long):
        pp = pprint.PrettyPrinter(indent=4, width=80, compact=False, sort_dicts=False)

        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            print("success")
            return_link = response.json()
            print(return_link['value'][0]['Link'])
            data=requests.get(return_link['value'][0]['Link']).json()
            # with open('trafficflow.json') as f:
            #     data = json.load(f)

            trafficData = pd.json_normalize(data['Value'], meta=['LinkID', 'Date', "HourOfDate", "Volume", "StartLon", "StartLat", "EndLon", "EndLat", "RoadName", "RoadCat"])
            print(trafficData.duplicated(subset=["RoadName"]).sum())
            trafficData.drop_duplicates(subset=["RoadName"], inplace=True)
            print(len(trafficData))
            trafficData["mid_lat"] = (trafficData["StartLat"].astype(float)+trafficData["EndLat"].astype(float))
            trafficData["mid_lon"] = (trafficData["StartLon"].astype(float)+trafficData["EndLon"].astype(float))
            print (len(trafficData))
            self.knr_model(trafficData)

            return trafficData

            # if data is not None and 'value' in data:
            #     filtered_data = self.filter_traffic_data(data['value'], lat, long)
            #     return filtered_data
            # else:
            #     return None
        except requests.RequestException as e:
            print(f"Error fetching traffic data: {e}")
            return None
        
    def knr_model(self, data):
        x_train, x_test, y_train, y_test = model_selection.train_test_split(data.loc[:, ['mid_lat', 'mid_lon']], data['Volume'].astype(float), test_size=0.2, random_state=1)
        knr = KNeighborsRegressor(n_neighbors=len(x_train),
                                  weights='distance',  # Use distance weights
                                  metric='euclidean')
        scaler = StandardScaler()
        scaler.fit(x_train)
        x_train_scaled = scaler.transform(x_train)
        x_test_scaled = scaler.transform(x_test)

        print(y_train.info())
        print(y_train)
        print(x_train)
        print(x_train_scaled)
        print(x_test.info())
        knr.fit(x_train_scaled,y_train)
        x_test_pred = knr.predict(x_test_scaled)
        print(x_test_pred)
        print(y_test)
        r2 = r2_score(y_test, x_test_pred)
        print(r2)


    def filter_traffic_data(self, data, lat, long):
        # Initialize an empty list to store the filtered data
        filtered_data = []

        # Loop through each entry in the data
        for entry in data:
            start_lat = entry.get('StartLat')
            start_lon = entry.get('StartLong')
            end_lat = entry.get('EndLat')
            end_lon = entry.get('EndLong')

            # Check if all required data is available
            if start_lat is not None and start_lon is not None and end_lat is not None and end_lon is not None:
                # Calculate the distance between the provided coordinates and the traffic entry coordinates
                distance = self.calculate_distance(lat, long, start_lat, start_lon)

                # Add the entry to the filtered data if it is within a certain radius of the provided coordinates
                if distance <= 1.0:  # Adjust the radius as needed
                    filtered_data.append(entry)

        # Return the filtered data
        return filtered_data

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        # Implement the calculation of Euclidean distance between coordinates
        return np.linalg.norm(np.subtract(np.array([lat1, lon1]), np.array([lat2, lon2])))

# Example usage
traffic_pipeline = TrafficFlowPipeline()
traffic_data = traffic_pipeline.get_traffic_data_as_user()

if traffic_data is not None:
    print("Traffic data retrieved successfully.")
else:
    print("Failed to retrieve traffic data.")