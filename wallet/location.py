from .wict import Wict

###########################################################

class Location(Wict):
    """
        Describes a location that can be attached to a pass/template

         "longitude":-122.374,
         "latitude":37.618,
         "relevantText":"Hello loc0",
         "streetAddress1":"address line #1",
         "streetAddress2":"address line #2",
         "city":"Palo Alto",
         "region":"CA",
         "regionCode":"94404",
         "country":"US"
    """

    def __init__(self, longitude, latitude, text, street_address_1=None, street_address_2=None, city=None, region=None,
                 region_code=None, country=None):
        super(Location, self).__init__()
        self.longitude = longitude
        self.latitude = latitude
        self.text = text
        self.street_address_1 = street_address_1
        self.street_address_2 = street_address_2
        self.city = city
        self.region = region
        self.region_code = region_code
        self.country = country
        self.set('id', None)

    @property
    def id(self):
        return self.val('id')

    @property
    def longitude(self):
        return self.val('longitude')

    @longitude.setter
    def longitude(self, longitude):
        self.set('longitude', longitude)

    @property
    def latitude(self):
        return self.val('latitude')

    @latitude.setter
    def latitude(self, latitude):
        self.set('latitude', latitude)

    @property
    def text(self):
        return self.val('relevantText')

    @text.setter
    def text(self, text):
        self.set('relevantText', text)

    @property
    def street_address_1(self):
        return self.val('streetAddress1')

    @street_address_1.setter
    def street_address_1(self, street_address_1):
        self.set('streetAddress1', street_address_1)

    @property
    def street_address_2(self):
        return self.val('streetAddress2')

    @street_address_2.setter
    def street_address_2(self, street_address_2):
        self.set('streetAddress2', street_address_2)

    @property
    def city(self):
        return self.val('city')

    @city.setter
    def city(self, city):
        self.set('city', city)

    @property
    def region(self):
        return self.val('region')

    @region.setter
    def region(self, region):
        self.set('region', region)

    @property
    def region_code(self):
        return self.val('regionCode')

    @region_code.setter
    def region_code(self, region_code):
        self.set('regionCode', region_code)

    @property
    def country(self):
        return self.val('country')

    @country.setter
    def country(self, country):
        self.set('country', country)

    @classmethod
    def from_dict(cls, obj_dict):
        ret = cls(longitude=None, latitude=None, text=None)
        ret.unpack_dict(obj_dict)
        return ret

###########################################################
