from urbanairship import common

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
        return resp.json()

    def coordinates_lookup(self, latitude, longitude, location_type):
        if not isinstance(latitude, int) or not isinstance(longitude, int):
           raise TypeError('latitude and longitude need to be numbers')

        url = common.LOCATION_URL + str(latitude) + ',' + str(longitude)
        params = None
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
        if not isinstance(lat1, int) or not isinstance(lat2, int) or \
                not isinstance(long1, int) or not isinstance(long2, int):
           raise TypeError('lat1, long1, lat2, and long2 need to be numbers')
        url = common.LOCATION_URL + lat1.to_s + ',' + long1.to_s + ',' + lat2.to_s + ',' + long2.to_s
        params = None
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
        url = common.LOCATION_URL
        if from_alias.kind_of? Array
          from_alias.each do |a|
            url += a + '&'
          end
          url = url.chop
        else
          url += from_alias
        end

        resp = @client.send_request(
          method: 'GET',
          url: url
        )
        logger.info("Retrieved location info from alias #{from_alias}")
        resp
      end

      def polygon_lookup(polygon_id: required('polygon_id'), zoom: required('zoom'))
        fail ArgumentError, 'polygon_id needs to be a string' unless polygon_id.is_a? String
        fail ArgumentError, 'zoom needs to be an integer' unless zoom.is_a? Integer

        url = LOCATION_URL + polygon_id + '?zoom=' + zoom.to_s
        resp = @client.send_request(
          method: 'GET',
          url: url
        )
        logger.info("Retrieved location info for polygon #{polygon_id} and zoom level #{zoom}")
        resp
      end