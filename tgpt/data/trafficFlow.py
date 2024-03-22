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
        self.headers = {'AccountKey': "Ilc7MV9DS/2/kLy1NxaEzQ==", "accept": "application/json"}
        # self.n_core = p.cpu_count() // 2

    def get_traffic_data_as_user(self, user):
        # lat, long = self.get_user_lat_long()
        vol = self.get_traffic_data(user)
        return vol

    def get_user_lat_long(self):
        user_location = geocoder.ip("me")
        if user_location.ok:
            return user_location.latlng
        else:
            print("Failed to retrieve user's location.")
            return None

    def get_traffic_data(self, user):
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
            trafficData["mid_lat"] = (trafficData["StartLat"].astype(float)+trafficData["EndLat"].astype(float)/2)
            trafficData["mid_lon"] = (trafficData["StartLon"].astype(float)+trafficData["EndLon"].astype(float)/2)
            dataMid=trafficData[["mid_lat", "mid_lon"]].copy()
            results = trafficData[["Volume"]].copy()
            user_mid=[(user[0]+user[2])/2, (user[1]+user[3])/2]
            print(user_mid)
            vol = self.knr_model(dataMid,results, user_mid)
            return vol


            # if data is not None and 'value' in data:
            #     filtered_data = self.filter_traffic_data(data['value'], lat, long)
            #     return filtered_data
            # else:
            #     return None
        except requests.RequestException as e:
            print(f"Error fetching traffic data: {e}")
            return None
        
    def knr_model(self, data, results, user):
        x_train, x_test, y_train, y_test = model_selection.train_test_split(data, results.astype(float), test_size=0.2, random_state=1)
        knr = KNeighborsRegressor(n_neighbors=len(x_train),
                                  weights='distance',  # Use distance weights
                                  metric='euclidean')
        scaler = StandardScaler()
        scaler.fit(x_train)
        x_train_scaled = scaler.transform(x_train)

        knr.fit(x_train_scaled,y_train)
        pred = knr.predict([user])
        # print(pred[0][0])
        return pred[0][0]
        


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
traffic_data = traffic_pipeline.get_traffic_data_as_user([1.3272336, 104,1.3117715, 102])

if traffic_data is not None:
    print("Traffic data retrieved successfully.")
else:
    print("Failed to retrieve traffic data.")

# class TrafficFlowPipeline:
#     def __init__(self):
#         self.url = "http://datamall2.mytransport.sg/ltaodataservice/TrafficFlow"
#         self.headers = {'AccountKey': "x4HdA6VGRTWtX3z/OUj8lA==", "accept": "application/json"}

#     def get_traffic_data(self, lat, long):
#         try:
#             # Fetch traffic flow data from the specified URL
#             response = requests.get(self.url, headers=self.headers)
#             response.raise_for_status()
#             data = response.json()

#             if data is not None and 'value' in data:
#                 # Filter traffic data based on the provided latitude and longitude
#                 filtered_data = self.filter_traffic_data(data['value'], lat, long)
#                 return filtered_data
#             else:
#                 return None
#         except requests.RequestException as e:
#             print(f"Error fetching data: {e}")
#             return None

#     def filter_traffic_data(self, data, lat, long):
#         # Initialize an empty list to store the filtered data
#         filtered_data = []

#         # Loop through each entry in the data
#         for entry in data:
#             # Extract start latitude, start longitude, end latitude, and end longitude from the entry
#             start_lat = entry.get('StartLat')
#             start_lon = entry.get('StartLong')
#             end_lat = entry.get('EndLat')
#             end_lon = entry.get('EndLong')

#             # Check if all required data is available
#             if start_lat is not None and start_lon is not None and end_lat is not None and end_lon is not None:
#                 # Calculate the distance between the provided coordinates and the traffic entry coordinates
#                 distance = self.calculate_distance(lat, long, start_lat, start_lon)

#                 # Add the entry to the filtered data if it is within a certain radius of the provided coordinates
#                 if distance <= 1.0:  # Adjust the radius as needed
#                     filtered_data.append(entry)

#         # Return the filtered data
#         return filtered_data

#     def calculate_distance(self, lat1, lon1, lat2, lon2):
#         # Convert latitude and longitude to radians
#         lat1_rad = np.radians(lat1)
#         lon1_rad = np.radians(lon1)
#         lat2_rad = np.radians(lat2)
#         lon2_rad = np.radians(lon2)

#         # Calculate the differences in coordinates
#         delta_lat = lat2_rad - lat1_rad
#         delta_lon = lon2_rad - lon1_rad

#         # Calculate the Euclidean distance
#         distance = np.sqrt(delta_lat**2 + delta_lon**2)

#         # Return the distance
#         return distance
    
#     #  def calculate_distance(self, lat1, lon1, lat2, lon2):
#     #     # Implement the calculation of Euclidean distance between coordinates
#     #     return np.linalg.norm(np.subtract(np.array([lat1, lon1]), np.array([lat2, lon2])))



# # Example usage
# traffic_pipeline = TrafficFlowPipeline()
# traffic_data = traffic_pipeline.get_traffic_data(1.3583564, 103.9420958)  # Pass latitude and longitude as arguments

# if traffic_data is not None:
#     print("Traffic data retrieved successfully.")
# else:
#     print("Failed to retrieve traffic data.")

