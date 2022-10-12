
from dataclasses import dataclass
from typing import Callable, Generic, Optional, TypeVar

DataClassT = TypeVar('DataClassT')
FieldTypeT = TypeVar('FieldTypeT')
StructTypeT = TypeVar('StructTypeT', bytes, float, int, bool)


@dataclass
class FieldStruct(Generic[FieldTypeT, StructTypeT]):
    fmt: str
    encoder: Optional[Callable[[FieldTypeT], StructTypeT]] = None
    decoder: Optional[Callable[[StructTypeT], FieldTypeT]] = None
