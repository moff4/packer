
from unittest import TestCase
from dataclasses import dataclass


from binary_packer import PackerFactory, int_field_struct, float_field_struct


@dataclass
class A:
    a: int = 0
    b: float = 1.2


class TestFieldStructs(TestCase):

    def test_all_fields(self):
        packer = PackerFactory(
            A,
            a=int_field_struct(size_in_bytes=1),
            b=float_field_struct(size_in_bytes=7),
        ).make_packer('a', 'b')

        obj = A(a=12, b=11.11)
        data = packer.pack(obj)

        self.assertIsInstance(data, bytes)

        obj2 = packer.unpack(data)

        self.assertIsInstance(obj2, A)
        self.assertEqual(obj, obj2)

    def test_part_fields(self):
        packer = PackerFactory(
            A,
            a=int_field_struct(size_in_bytes=1),
            b=float_field_struct(size_in_bytes=7),
        ).make_packer('a')

        obj = A(a=12, b=11.11)
        data = packer.pack(obj)

        self.assertIsInstance(data, bytes)

        obj2 = packer.unpack(data)

        self.assertIsInstance(obj2, A)
        self.assertNotEqual(obj, obj2)
        self.assertEqual(obj.a, obj2.a)
        self.assertNotEqual(obj.b, obj2.b)
