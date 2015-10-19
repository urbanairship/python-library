import json
import gzip
import collections
import datetime
from urbanairship import common

CHUNK = 16 * 1024


class StaticList(object):
    def __init__(self, airship, name):
        self.airship = airship
        self.name = name
        self.description = None
        self.extra = None

    def create(self):
        """Create a static list

        :param description: An optional user-provided description of the list.
            Maximum length of 1000 characters
        :param extra: An optional user-provided JSON map of string values associated
            with a list. A key has a maximum length of 64 characters, while a value can
            be up to 1024 characters. You may add up to 100 key-value pairs.
        :return:
        """

        payload = {'name': self.name}
        if self.description is not None:
            payload['description'] = self.description
        if self.extra is not None:
            payload['extra'] = self.extra

        body = json.dumps(payload).encode('utf-8')
        response = self.airship._request(
            'POST',
            body,
            common.LISTS_URL,
            'application/json',
            version=3
        )
        return response.json()

    def upload(self, csv_file):
        """Upload a CSV file to a static list

        :param csv_file: open file descriptor with two column format: identifier_type, identifier
        :return: http response
        """

        zipped = GzipCompressReadStream(csv_file)
        url = common.LISTS_URL + self.name + '/csv/'
        response = self.airship._request(
            method='PUT',
            body=zipped,
            url=url,
            content_type='text/csv',
            version=3,
            encoding='gzip'
        )
        return response.json()

    def update(self):
        """Update the metadata in a static list

        :param description: Description of the list (optional)
        :param extra: JSON map of string values to associate with the list
        :return: http response
        """

        if self.description is None and self.extra is None:
            raise ValueError('Either description or extra must be non-empty.')
        payload = {}
        if self.description is not None:
            payload['description'] = self.description
        if self.extra is not None:
            payload['extra'] = self.extra
        body = json.dumps(payload).encode('utf-8')
        url = common.LISTS_URL + self.name
        response = self.airship._request('PUT', body, url, 'application/json', version=3)
        return response.json()

    @classmethod
    def from_payload(cls, payload, airship):
        obj = cls(airship, payload['name'])
        for key in payload:
            if key in 'created' or key in 'last_updated':
                payload[key] = datetime.datetime.strptime(
                    payload[key], '%Y-%m-%dT%H:%M:%S'
                )
            setattr(obj, key, payload[key])
        return obj

    def lookup(self):
        """
        :return: Information about the static list
        """

        url = common.LISTS_URL + self.name
        response = self.airship._request('GET', None, url, version=3)
        payload = response.json()
        return self.from_payload(payload, self.airship)

    def delete(self):
        """
        :return: Delete the static list
        """
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


class Buffer(object):
    def __init__(self):
        self.__buf = collections.deque()
        self.__size = 0

    def __len__(self):
        return self.__size

    def write(self, data):
        self.__buf.append(data)
        self.__size += len(data)

    def read(self, size):
        ret_list = []
        while size > 0 and len(self.__buf):
            chunk_of_file = self.__buf.popleft()
            size -= len(chunk_of_file)
            ret_list.append(chunk_of_file)
        if size < 0:
            ret_list[-1], remainder = ret_list[-1][:size], ret_list[-1][size:]
            self.__buf.appendleft(remainder)
        ret = ''.join(ret_list)
        self.__size -= len(ret)
        return ret

    def flush(self):
        pass

    def close(self):
        pass


class GzipCompressReadStream (object):
    def __init__(self, file_obj):
        self.__input = file_obj
        self.__buf = Buffer()
        self.__gzip = gzip.GzipFile(None, mode='wb', fileobj=self.__buf)
        self.is_finished = False

    def read(self, size):
        while len(self.__buf) < size:
            chunk_of_file = self.__input.read(CHUNK)
            if not chunk_of_file:
                self.__gzip.close()
                self.is_finished = True
                break
            self.__gzip.write(chunk_of_file)
            self.__gzip.flush()
        return self.__buf.read(size)

    def __iter__(self):
        return self

    def __next__(self):
        if self.is_finished is True:
            raise StopIteration
        else:
            return self.read(CHUNK)

    def next(self):
        return self.__next__()
