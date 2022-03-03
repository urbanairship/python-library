import json
from typing import Dict, Optional, Any, List

from requests import Response

from urbanairship import Airship
from urbanairship.devices.static_lists import GzipCompressReadStream


class TagList:
    """Create, Upload, Delete, and get information for a tag list.
    Please see the Airship API documentation for more information
    about CSV formatting, limits, and use of this feature.

    ;param airship: Required. An urbanairship.Airship instance.
    :param list_name: Required. A name for the list this instance represents.
    :param description: Optional. A description of the list.
    :param extra: Optional. A a dictionary of string mappings associated with the list.
    :param add_tags: Optional. A dictionary consisting of a tag group string and list of tag
    string to add to uploaded channels.
    :param remove_tags: Optional. A dictionary consisting of a tag group string and list of
    tag strings to remove from uploaded channels.
    :param set_tags: Optional. A dictionary consisting of a tag group string and list of tag
    strings to set on uploaded channels. Warning: This action is destructive and will
    remove all existing tags associated with channels.
    """

    def __init__(
        self,
        airship: Airship,
        list_name: str,
        description: Optional[str] = None,
        extra: Optional[Dict[str, str]] = None,
        add_tags: Optional[Dict[str, List[str]]] = None,
        remove_tags: Optional[Dict[str, List[str]]] = None,
        set_tags: Optional[Dict[str, List[str]]] = None,
    ) -> None:
        self.airship = airship
        self.list_name = list_name
        self.description = description
        self.extra = extra
        self.add_tags = add_tags
        self.remove_tags = remove_tags
        self.set_tags = set_tags

    @property
    def _create_payload(self) -> Dict:
        payload: Dict[str, Any] = {"name": self.list_name}

        if self.description:
            payload["description"] = self.description
        if self.extra:
            payload["extra"] = self.extra
        if self.add_tags:
            payload["add"] = self.add_tags
        if self.remove_tags:
            payload["remove"] = self.remove_tags
        if self.set_tags:
            payload["set"] = self.set_tags

        return payload

    def create(self) -> Response:
        """Create a new tag list. Channels must be uploaded after creation using
        the `upload` method.

        :return: Response object
        """
        response = self.airship.request(
            method="POST",
            url=self.airship.urls.get("tag_lists_url"),
            body=json.dumps(self._create_payload),
            content_type="application/json",
            version=3,
        )

        return response

    def upload(self, file_path: str) -> Response:
        """Upload a CSV file of channels. See the Airship API documentation
        for information about CSV file formatting requirements and limits.

        :param file_path: Path to the CSV file to upload.

        :return: Response object
        """
        with open(file_path, "rb") as open_file:
            response = self.airship.request(
                method="PUT",
                body=GzipCompressReadStream(open_file),
                url=f"{self.airship.urls.get('tag_lists_url')}/{self.list_name}/csv",
                content_type="text/csv",
                version=3,
                encoding="gzip",
            )
        return response

    def get_errors(self) -> Response:
        """Returns a csv of tag list processing errors.

        :return: Response object
        """
        response = self.airship.request(
            method="GET",
            body={},
            url=f"{self.airship.urls.get('tag_lists_url')}/{self.list_name}/errors",
            version=3,
        )
        return response

    @classmethod
    def list(cls, airship: Airship) -> Response:
        """Returns a json string with details on all tag lists associated with
        an Airship instance / project.

        :return: Response object
        """
        response = airship.request(
            method="GET", body={}, url=airship.urls.get("tag_lists_url"), version=3
        )
        return response
