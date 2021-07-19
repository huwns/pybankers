import unittest

from bankers import Tile


class TestTile(unittest.TestCase):

    def test_sairei(self):
        tile = Tile('祭礼', 'sairei')
        ans = tile.getMove(None, 20)
        if ans > 0:
            self.assertTrue(ans % 2 == 0)
        else:
            self.assertTrue(ans % 2 == 1)


