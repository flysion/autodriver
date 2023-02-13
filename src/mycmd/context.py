class Context:
    def __init__(self, items: dict = {}, attrs: dict = {}):
        self.__dict__['_attrs'] = attrs
        self.__dict__['_items'] = items

    def __getattr__(self, key):
        return self._attrs[key]

    def __setattr__(self, key, value):
        self._attrs[key] = value

    def __getitem__(self, key):
        value = self._items[key]
        if callable(value):
            return value()
        else:
            return value

    def __setitem__(self, key, value):
        self._items[key] = value

    def __contains__(self, key):
        if key in self._items:
            return True
        else:
            return False
