from urbanairship import common
import logging

logger = logging.getLogger('urbanairship')


class LocationFinder(object):
    def __init__(self, airship):
        self.airship = airship

    def name_lookup(self, name, location_type=None):
        """Lookup a location by name

        :param name: Name of the location to look up
        :param location_type: Location type
        :return: Information about the location
        """

        params = {'q': name}

        if location_type:
            params['type'] = location_type

        resp = self.airship._request(
            'GET',
            None,
            common.LOCATION_URL,
            version=3,
            params=params
        )
        logger.info(u'Retrieved location info by name: %s' % name)
        return resp.json()

    def coordinates_lookup(self, latitude, longitude, location_type=None):
        """Lookup a location by coordinates

        :param latitude: Latitude of the location
        :param longitude: Longitude of the location
        :param location_type: Type of the location (optional)
        :return: Information about the location
        """

        coor_are_valid = isinstance(latitude, (int, float)) and isinstance(longitude, (int, float))

        if not coor_are_valid:
            raise TypeError('latitude and longitude need to be numbers')

        url = '{base_url}{latitude},{longitude}'.format(
            base_url=common.LOCATION_URL,
            latitude=str(latitude),
            longitude=str(longitude))

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
        logger.info('Retrieved location info by coordinates: %s,%s' % (
            str(latitude), str(longitude)))
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

        loc1_valid = isinstance(lat1, (float, int)) and isinstance(long1, (float, int))
        loc2_valid = isinstance(lat2, (float, int)) and isinstance(long2, (float, int))

        if not loc1_valid or not loc2_valid:
            raise TypeError('lat1, long1, lat2, and long2 need to be numbers')

        url = '{base_url}{lat1},{long1},{lat2},{long2}'.format(
            base_url=common.LOCATION_URL,
            lat1=str(lat1),
            long1=str(long1),
            lat2=str(lat2),
            long2=str(long2)
        )
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
        logger.info(
            'Retrieved location info by bounding box: %s,%s,%s,%s' % (
                str(lat1), str(long1), str(lat2), str(long2)))
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
        logger.info('Retrieved location info by alias: %s' % from_alias)
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
        logger.info('Retrieved location info by polygon id: %s and zoom: %s' % (
            polygon_id, str(zoom)))
        return resp.json()

    def date_ranges(self):
        resp = self.airship._request(
            'GET',
            None,
            common.SEGMENTS_URL + 'dates/',
            version=3,
        )
        return resp.json()
