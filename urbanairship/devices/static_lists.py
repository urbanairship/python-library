import json
import gzip
import collections
import datetime
from typing import Dict, Optional
from io import TextIOWrapper

from requests import Response

from urbanairship import common, Airship

CHUNK = 16 * 1024


class StaticList:
    def __init__(self, airship: Airship, name: str) -> None:
        self.airship = airship
        self.name = name
        self.description = None
        self.extra = None

    def create(self) -> Dict:
        """Create a Static List"""
        payload = {"name": self.name}
        if self.description is not None:
            payload["description"] = self.description
        if self.extra is not None:
            payload["extra"] = self.extra

        body = json.dumps(payload)
        response = self.airship._request(
            method="POST",
            body=body,
            url=self.airship.urls.get("lists_url"),
            content_type="application/json",
            version=3,
        )
        return response.json()

    def upload(self, csv_file: TextIOWrapper) -> Dict:
        """Upload a CSV file to a static list

        :param csv_file: open file descriptor with two column format:
            identifier_type, identifier

        :return: http response
        """

        zipped = GzipCompressReadStream(csv_file)
        url = self.airship.urls.get("lists_url") + self.name + "/csv/"
        response = self.airship._request(
            method="PUT",
            body=zipped,
            url=url,
            content_type="text/csv",
            version=3,
            encoding="gzip",
        )
        return response.json()

    def update(self) -> Dict:
        """Update the metadata in a static list

        :return: http response
        """

        if self.description is None and self.extra is None:
            raise ValueError("Either description or extra must be non-empty.")

        payload = {}

        if self.description is not None:
            payload["description"] = self.description
        if self.extra is not None:
            payload["extra"] = self.extra

        body = json.dumps(payload).encode("utf-8")
        url = self.airship.urls.get("lists_url") + self.name

        response = self.airship._request(
            "PUT", body, url, "application/json", version=3
        )

        return response.json()

    @classmethod
    def download(cls, airship: Airship, list_name: str) -> Response:
        """
        Allows you to download the contents of a static list. Alias and named_user
        values are resolved to channels.

        :param airship: Required. An urbanairship.Airship instance.
        :param list_name: Required. Name of an existing list to download.

        :return: csv list data
        """
        response = airship._request(
            method="GET",
            url=airship.urls.get("lists_url") + list_name + "/csv/",
            body={},
        )

        return response

    @classmethod
    def from_payload(cls, payload: Dict, airship: Airship):
        for key in payload:
            if key in "created" or key in "last_updated":
                payload[key] = datetime.datetime.strptime(
                    payload[key], "%Y-%m-%dT%H:%M:%S"
                )
            setattr(cls, key, payload[key])
        return cls

    def lookup(self):
        """
        Get Information about the static list

        :return: urbanairship.StaticList objects
        """

        url = self.airship.urls.get("lists_url") + self.name
        response = self.airship._request("GET", None, url, version=3)
        payload = response.json()
        return self.from_payload(payload, self.airship)

    def delete(self) -> Response:
        """
        Delete the static list
        """
        url = self.airship.urls.get("lists_url") + self.name
        return self.airship._request("DELETE", None, url, version=3)


class StaticLists(common.IteratorParent):
    next_url: Optional[str] = None
    data_attribute: str = "lists"

    def __init__(self, airship):
        """Gets an iterable listing of existing static lists"""
        self.next_url = airship.urls.get("lists_url")
        super(StaticLists, self).__init__(airship, None)


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
        ret = b"".join(ret_list)
        self.__size -= len(ret)
        return ret

    def flush(self):
        pass

    def close(self):
        pass


class GzipCompressReadStream(object):
    def __init__(self, file_obj):
        self.__input = file_obj
        self.__buf = Buffer()
        self.__gzip = gzip.GzipFile(None, mode="wb", fileobj=self.__buf)
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
