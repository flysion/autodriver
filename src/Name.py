class Name(str):
    def __new__(cls, value, id=None):
        return str.__new__(cls, value)

    def __init__(self, value, id=None):
        self._id = id

    def new(self, value):
        return Name(value, id=self._id)

    def id(self):
        return self._id
