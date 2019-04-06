import unittest
from BalancedBSTSet import BalancedBSTSet


class TestBalancedBSTSet(unittest.TestCase):
    def setUp(self):
        self.bst = BalancedBSTSet()
        self.r = self.bst.add(5)
        self.a = self.bst.add(3)
        self.b = self.bst.add(7)
        self.ba = self.bst.add(6)
        self.bb = self.bst.add(8)

    def test_children(self):
        self.assertEqual(self.r.left, self.a)
        self.assertEqual(self.r.right, self.b)
        self.assertEqual(self.b.left, self.ba)
        self.assertEqual(self.b.right, self.bb)


if __name__ == '__main__':
    unittest.main()