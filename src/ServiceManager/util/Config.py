from enum import Enum


class OrderedEnum(Enum):
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


class LogLevel(OrderedEnum):
    DEBUG = 1
    ERROR = 2
    INFO = 3
    NOLOG = 4


def checkKeyInDict(key, dictionary, types):
    """
    checks if a dict has a given key and if the key has the correct type

    :param key: key to check in the given dict => dictionary[key]
    :param dictionary: dict to check
    :param types: a list of valid types
    :return: True if key is valid, raises KeyError or TypeError if key is invalid
    """

    if key in dictionary:
        if isinstance(dictionary[key], types):
            return True
        else:
            raise TypeError(f"{dictionary[key]} is not instanceof {types}, but {type(dictionary[key])}")
    else:
        raise KeyError(f"{key} is not in dictionary!")
