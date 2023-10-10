from collections import namedtuple
from typing import Tuple, Type


class ObjectMappingHelper():

    def fromDict(self, input: dict, schemaName: str) -> Type[Tuple]:
        return namedtuple(schemaName, input.keys())(*input.values())
