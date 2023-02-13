class UserData:
    def __init__(self):
        self._items = {}

    def __getitem__(self, key):
        return self._items[key]

    def __setitem__(self, key, value):
        self._items[key] = value

    def __delitem__(self, key):
        del self._items[key]

    def __contains__(self, key):
        return key in self._items
