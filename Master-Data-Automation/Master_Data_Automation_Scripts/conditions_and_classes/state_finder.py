import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut


class StateFinder:
    def __init__(self, sheets_dict):
        self.sheets_dict = sheets_dict

    def get_state(address):
        try:
            geolocator = Nominatim(user_agent="geoapiExercises")  # Initialize geocoder
            location = geolocator.geocode(address, timeout=10)    # Geocode address
            if location and location.raw.get('address'):
                return location.raw['address'].get('state')       # Extract state
        except GeocoderTimedOut:
            return None
        return None