import requests
import math
import os

class RoadworkPipeline:
    def __init__(self, data):
        self.data = data['value']

    def get_nearest_roadwork(self, lat, long):
        # Initialize variables to store the nearest roadwork incident and its distance
        nearest_distance = float('inf')
        nearest_roadwork = None

        # Iterate over each roadwork incident
        for incident in self.data:
            # Extract latitude, longitude, and message of the incident
            incident_lat = incident['Latitude']
            incident_long = incident['Longitude']
            message = incident['Message']

            # Calculate the distance between the provided coordinates and the incident coordinates
            distance = self.calculate_distance(lat, long, incident_lat, incident_long)

            # Update nearest roadwork if this incident is closer
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_roadwork = message

        return nearest_roadwork

    def calculate_distance(self, lat1, long1, lat2, long2):
        # Convert latitude and longitude from degrees to radians
        lat1_rad = math.radians(lat1)
        long1_rad = math.radians(long1)
        lat2_rad = math.radians(lat2)
        long2_rad = math.radians(long2)

        # Calculate the differences in coordinates
        delta_lat = lat2_rad - lat1_rad
        delta_long = long2_rad - long1_rad

        # Calculate the great-circle distance using Haversine formula
        a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_long / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = 6371 * c  # Earth radius in kilometers

        return distance

# Fetch data from the pipeline
def fetch_pipeline_data():
    url = "http://datamall2.mytransport.sg/ltaodataservice/IncidentSet()"
    headers = {'AccountKey': os.environ.get("LTA_KEY"), "accept": "application/json"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching pipeline data: {e}")
        return None

# Prompt user for latitude and longitude coordinates
def get_user_coordinates():
    lat = float(input("Enter latitude: "))
    long = float(input("Enter longitude: "))
    return lat, long

# Main function
def main():
    # Fetch pipeline data
    pipeline_data = fetch_pipeline_data()
    if pipeline_data is None:
        print("Failed to fetch pipeline data. Exiting.")
        return

    # Create RoadworkPipeline instance
    roadwork_pipeline = RoadworkPipeline(pipeline_data)

    # Get user coordinates
    user_lat, user_long = get_user_coordinates()

    # Get the nearest roadwork message for provided coordinates
    nearest_message = roadwork_pipeline.get_nearest_roadwork(user_lat, user_long)
    if nearest_message:
        print("Nearest roadwork message:", nearest_message)
    else:
        print("No roadwork incidents found nearby.")

if __name__ == "__main__":
    main()
