import json


class Wict(object):
    """
        This is the base object for most of the high level objects
        It encapsulates a dictionary that hosts the objects structure
    """

    def __init__(self):
        self._dict = dict()

    def val(self, key):
        ret = self._dict.get(key)
        return ret

    def set(self, key, val):
        if val is None:
            if self._dict.has_key(key):
                self._dict.pop(key)
        else:
            self._dict[key] = val

    def has_key(self, key):
        return key in self._dict

    def unpack_dict(self, dictionary):
        self._dict = dictionary

    def get_dict(self):
        return self._dict

    def to_json(self):
        return json.dumps(self._dict)

    def __str__(self):
        return json.dumps(self._dict, sort_keys=True, indent=4, separators=(',', ': '))
