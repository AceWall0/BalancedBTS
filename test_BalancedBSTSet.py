import unittest
from BalancedBSTSet import BalancedBSTSet


class TestBalancedBSTSet(unittest.TestCase):
    def setUp(self):
        self.bst = BalancedBSTSet(False)
        self.bst.add(3)
        self.bst.add(1)
        self.bst.add(7)
        self.bst.add(6)
        self.bst.add(8)

    def test_add(self):
        self.assertEqual(self.bst.root().data, 3)
        self.assertEqual(self.bst.root().left.data, 1)
        self.assertEqual(self.bst.root().right.left.data, 6)
        self.assertEqual(self.bst.root().right.right.data, 8)

    def test_repr(self):
        self.assertEqual(
            repr(self.bst),
            (
                "+ 3\n"
                "  - 1\n"
                "  + 7\n"
                "    - 6\n"
                "    - 8\n"
            )
        )

    def test_remove(self):
        self.bst.remove(7)
        self.assertEqual(self.bst.root().right.data, 8)
        self.bst.remove(8)
        self.assertEqual(self.bst.root().right.data, 6)
        self.bst.remove(3)
        self.assertEqual(self.bst.root().data, 6)

    def test_rebalance(self):
        self.bst.add(9)
        self.bst.add(10)
        self.bst.add(11)
        self.bst.rebalance()
        self.assertEqual(
            repr(self.bst),
            (
                "+ 8\n"
                "  + 6\n"
                "    + 3\n"
                "      - 1\n"
                "      -\n"
                "    - 7\n"
                "  + 10\n"
                "    - 9\n"
                "    - 11\n"
            )
        )


if __name__ == '__main__':
    unittest.main()