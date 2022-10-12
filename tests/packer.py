
from unittest import TestCase
from dataclasses import dataclass


from binary_packer import PackerFactory, FieldStruct


@dataclass
class A:
    a: int = 0
    b: float = 1.2


class TestPacker(TestCase):

    def test_all_fields(self):
        packer = PackerFactory(
            A,
            a=FieldStruct('b'),
            b=FieldStruct('d'),
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
            a=FieldStruct('b'),
            b=FieldStruct('d'),
        ).make_packer('a')

        obj = A(a=12, b=11.11)
        data = packer.pack(obj)

        self.assertIsInstance(data, bytes)

        obj2 = packer.unpack(data)

        self.assertIsInstance(obj2, A)
        self.assertNotEqual(obj, obj2)
        self.assertEqual(obj.a, obj2.a)
        self.assertNotEqual(obj.b, obj2.b)
