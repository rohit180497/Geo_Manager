import pandas as pd
import numpy as np
from collections import defaultdict
import inspect
import os

from math import radians, cos, sin, asin, sqrt


class GeoManager:

    def __init__(self) -> None:
        self.geo_df = pd.read_json(os.path.dirname(
            inspect.getfile(GeoManager)), 'static\heocode.json')
        self.geo_df['latitude'] = self.geo_df['latitude'].astype(float)
        self.geo_df['longitude'] = self.geo_df['longitude'].astype(float)

        self.latitude = defaultdict(GeoManager._default)
        self.longitude = defaultdict(GeoManager._default)
        self.county = defaultdict(GeoManager._default)
        self.state = defaultdict(GeoManager._default)

        geo_dict = self.geo_df.to_dict()

        self.latitude.update(geo_dict.get('latitude'))
        self.longitude.update(geo_dict.get('longitude'))
        self.county.update(geo_dict.get('county_name'))
        self.state.update(geo_dict.get('state_name'))

        self.v_get_lat_lon = np.vectorize(self._get_lat_lon)
        self.v_get_county_state = np.vectorize(self._get_county_state)

    @staticmethod
    def _default():
        return 0

    def _get_lat_lon(self, zip):
        lat = self.latitude.get(zip, 0)
        lon = self.longitude.get(zip, 0)

        return lat, lon

    def get_geo_df(self):
        return self.geo_df

    def get_lat_lon(self, zip):
        '''
        Given zip codes, the function returns geographical latitude and longitude of the same parameters 

        -----------
        zip : list or array like, zip codes of location

        returns
        -----------

        latitudes: series float, geographic latitude
        longitude: series float, geographic longitude

        '''
        return self.v_get_lat_lon(zip)

    def get_county_state(self, zip):
        '''
        Given zip codes, the function returns geographical county and state of the same parameters 

        -----------
        zip : list or array like, zip codes of location

        returns
        -----------

        county: series float, geographic county (district)
        state: series float, geographic state

        '''
        return self.v_get_county_state(zip)

    def _haversine(lat1, lon1, lat2, lon2):
        R = 6372.8

        dLat = radians(lat2 - lat1)
        dLon = radians(lon2 - lon1)
        lat1 = radians(lat1)
        lat2 = radians(lat2)

        a = sin(dLat/2)**2 + cos(lat1) * cos(lat2) * sin(dLon/2)**2
        c = 2 * asin(sqrt(a))

        return R * c

    _v_haversine = np.vectorize(_haversine)

    def get_flight_distance(self, zip1, zip2):
        '''
        Given zip codes, the function returns haversine distance in kms between the two locations   
        Parameters
        -----------
        zip1 : int, zip code of the first location
        zip2 : int, zip code of the second location

        returns
        -----------

        distance: float, kms between zip1 and zip2 

        '''
        lat1, lon1 = self.get_lat_lon(zip1)
        lat2, lon2 = self.get_lat_lon(zip2)

        return GeoManager._v_haversine(lat1, lon1, lat2, lon2)
