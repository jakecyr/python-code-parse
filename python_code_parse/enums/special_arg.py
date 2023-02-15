from enum import Enum, auto


class SpecialArg(Enum):
    kwarg = auto()
    vararg = auto()
    kwonlyargs = auto()
