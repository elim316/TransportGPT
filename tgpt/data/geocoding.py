from geopy.geocoders import Nominatim
from geopy.distance import geodesic

class Geocoder:

    def getLocation(cls, loc_name):
        geolocator = Nominatim(user_agent="geolocator")
        location = geolocator.geocode(loc_name)
        print(location.raw)
        return None
