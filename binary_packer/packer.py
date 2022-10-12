from struct import Struct
from typing import Any, Type

from .types import DataClassT, FieldStruct


def build_struct_format(fields_structs: list[tuple[str, FieldStruct[Any, Any]]]) -> str:
    return ''.join(field_struct.fmt for _, field_struct in fields_structs)


class Packer:
    """
    Этот класс предполагается приватным, поэтому настоятельно рекомендуется создавать его экземпляры
    исключительно через фабрику PackerFactory. Такой подход гарантирует консистентность пакера.
    """

    def __init__(self, target_cls: Type[DataClassT], fields_structs: list[tuple[str, FieldStruct[Any, Any]]]) -> None:
        self._target_cls = target_cls
        self._fields_structs = fields_structs

        item_schema = build_struct_format(fields_structs)
        self.struct = Struct(item_schema)

    def pack(self, obj: DataClassT) -> bytes:
        encoded_values = []
        for field, struct_info in self._fields_structs:
            encode = struct_info.encoder
            encoded_values.append(
                getattr(obj, field)
                if encode is None else
                encode(getattr(obj, field))
            )

        return self.struct.pack(*encoded_values)

    def unpack(self, array: bytes) -> DataClassT:
        obj = {}
        for (field, struct_info), value in zip(self._fields_structs, self.struct.unpack(array)):
            decode = struct_info.decoder
            obj[field] = value if decode is None else decode(value)

        return self._target_cls(**obj)

    @property
    def size(self) -> int:
        return self.struct.size
