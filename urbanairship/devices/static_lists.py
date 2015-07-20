import json
from datetime import datetime

try:
    from cStringIO import StringIO      # Python 2.x
except ImportError:
    from io import BytesIO as StringIO  # Python 3.x

from urbanairship import common
from gzip import GzipFile


class StaticList(object):
    def __init__(self, airship, name):
        self.airship = airship
        self.name = name

    def create(self, description=None, extras=None):
        """Create a static list

        :param description: An optional user-provided description of the list.
            Maximum length of 1000 characters
        :param extras: An optional user-provided JSON map of string values associated
            with a list. A key has a maximum length of 64 characters, while a value can
            be up to 1024 characters. You may add up to 100 key-value pairs.
        :return:
        """

        payload = {'name': self.name}
        if description is not None:
            payload['description'] = description
        if extras is not None:
            payload['extras'] = extras

        body = json.dumps(payload).encode('utf-8')
        url = common.LISTS_URL
        response = self.airship._request('POST', body, url, 'application/json', version=3)
        return response.json()

    def upload(self, csv_file):
        """Upload a CSV file to a static list

        :param csv_file: open file descriptor with two column format: identifier_type, identifier
        :return: http response
        """

        # Gzip the csv file into a buffer
        fgz = StringIO()
        zipped = GzipFile(mode='wb', fileobj=fgz)
        zipped.writelines(csv_file)
        zipped.close()

        url = common.LISTS_URL + self.name + '/csv/'
        response = self.airship._request(
            method='PUT',
            body=fgz,
            url=url,
            content_type='text/csv',
            version=3,
            encoding='gzip'
        )
        fgz.close()
        return response.json()

    def update(self, description=None, extras=None):
        if description is None and extras is None:
            raise ValueError('Either description or extras must be non-empty.')
        payload = {}
        if description is not None:
            payload['description'] = description
        if extras is not None:
            payload['extras'] = extras
        body = json.dumps(payload).encode('utf-8')
        url = common.LISTS_URL + self.name
        response = self.airship._request('PUT', body, url, 'application/json', version=3)
        return response.json()

    @classmethod
    def from_payload(cls, payload, airship):
        obj = cls(airship, payload['name'])
        for key in payload:
            if key in 'created' or key in 'last_updated':
                payload[key] = datetime.strptime(
                    payload[key], '%Y-%m-%d %H:%M:%S'
                )
            setattr(obj, key, payload[key])
        return obj

    def lookup(self):
        url = common.LISTS_URL + self.name
        response = self.airship._request('GET', None, url, version=3)
        payload = response.json()
        return self.from_payload(payload, self.airship)

    def delete(self):
        url = common.LISTS_URL + self.name
        return self.airship._request('DELETE', None, url, version=3)


class StaticLists(object):
    start_url = common.LISTS_URL
    next_url = None
    start_date = None
    end_date = None
    data_attribute = 'lists'
    _page = None

    def __init__(self, airship):
        self._airship = airship
        self.next_url = self.start_url
        self._token_iter = iter(())

    def __iter__(self):
        return self

    def __next__(self):
        try:
            return StaticList.from_payload(next(self._token_iter), self._airship)
        except StopIteration:
            self._fetch_next_page()
            return StaticList.from_payload(next(self._token_iter), self._airship)

    def next(self):
        """Necessary for iteration to work with Python 2.*."""
        return self.__next__()

    def _fetch_next_page(self):
        if not self.next_url:
            return
        self._load_page(self.next_url)
        self.next_url = self._page.get('next_page')

    def _load_page(self, url):
        response = self._airship._request(
            method='GET',
            body=None,
            url=url,
            version=3,
        )
        self._page = page = response.json()
        self._token_iter = iter(page[self.data_attribute])

