class Context:
    def __init__(self, items: dict = None, attrs: dict = None):
        self.__dict__['_items_'] = items if items is not None else {}
        self.__dict__['_attrs_'] = attrs if attrs is not None else {}

    def __getattr__(self, key):
        return self._attrs_[key]

    def __setattr__(self, key, value):
        self._attrs_[key] = value

    def __getitem__(self, key):
        value = self._items_[key]
        if callable(value):
            return value()
        else:
            return value

    def __setitem__(self, key, value):
        self._items_[key] = value

    def __contains__(self, key):
        if key in self._items_:
            return True
        else:
            return False

    def items(self):
        return self._items_

    def attrs(self):
        return self._attrs_
