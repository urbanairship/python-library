from urbanairship import common
import logging
logger = logging.getLogger('urbanairship')

class Location(object):
    def __init__(self, airship):
        self.airship = airship

    def name_lookup(self, name, location_type=None):
        """Lookup a location by name

        :param name: Name of the location to lookup
        :param location_type: Location type
        :return: Information about the location
        """

        params = {
            'q': name
        }
        if location_type:
            params['type'] = location_type

        resp = self.airship._request(
            'GET',
            None,
            common.LOCATION_URL,
            version=3,
            params=params
        )
        logger.info('Retrieved location info by name %s', name)
        return resp.json()

    def coordinates_lookup(self, latitude, longitude, location_type=None):
        """Lookup a location by coordinates

        :param latitude: Latitude of the location
        :param longitude: Longitude of the location
        :param location_type: Type of the location (optional)
        :return: Information about the location
        """

        if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
            raise TypeError('latitude and longitude need to be numbers')

        url = common.LOCATION_URL + str(latitude) + ',' + str(longitude)
        params = {}
        if location_type:
            params['type'] = location_type
        resp = self.airship._request(
            'GET',
            None,
            url,
            version=3,
            params=params
        )
        return resp.json()

    def bounding_box_lookup(self, lat1, long1, lat2, long2, location_type=None):
        """Lookup a location by bounding box

        :param lat1: First latitude of the location
        :param long1: First longitude of the location
        :param lat2: Second latitude of the location
        :param long2: Second longitude of the location
        :param location_type: Type of the location (optional)
        :return: Information about the location
        """

        if not isinstance(lat1, (float, int)) or not isinstance(lat2, (float, int)) or \
                not isinstance(long1, (float, int)) or not isinstance(long2, (float, int)):
            raise TypeError('lat1, long1, lat2, and long2 need to be numbers')
        url = common.LOCATION_URL + str(lat1) + ',' + str(long1) + ',' + str(lat2) + ',' + str(long2)
        params = {}
        if location_type:
            params['type'] = location_type
        resp = self.airship._request(
            'GET',
            None,
            url,
            version=3,
            params=params
        )
        return resp.json()

    def alias_lookup(self, from_alias):
        """Lookup a location by alias or list of aliases
        :param from_alias: alias of the location
        :return: Information about the location
        """

        params = {}
        if isinstance(from_alias, list):
            for alias in from_alias:
                alias_parts = alias.split('=')
                params[alias_parts[0]] = alias_parts[1]
        else:
            alias_parts = from_alias.split('=')
            params[alias_parts[0]] = alias_parts[1]

        resp = self.airship._request(
            'GET',
            None,
            common.LOCATION_URL + 'from-alias',
            version=3,
            params=params
        )
        return resp.json()

    def polygon_lookup(self, polygon_id, zoom):
        """ Lookup the location by polygon id
        :param polygon_id: polygon id of the location
        :param zoom: zoom level of the desired location information
        :return: Information about the location
        """

        if not isinstance(zoom, int) or zoom < 1 or zoom > 20:
            raise TypeError('zoom needs to be an integer between 1 and 20')
        params = {'zoom': str(zoom)}
        resp = self.airship._request(
            'GET',
            None,
            common.LOCATION_URL + polygon_id,
            version=3,
            params=params
        )
        return resp.json()
