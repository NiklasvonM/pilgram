import unittest
from datetime import timedelta

import numpy as np

from pilgram.strings import rewards_string
from pilgram.utils import PathDict, generate_random_eldritch_name, read_update_interval


class TestUtils(unittest.TestCase):
    def test_pathdict(self):
        pd = PathDict({"a": 1, "b": 2, "c": 3, "d": {"e": 4}})
        self.assertEqual(pd.path_get("a"), 1)
        self.assertEqual(pd.path_get("b"), 2)
        self.assertEqual(pd.path_get("c"), 3)
        self.assertEqual(pd.path_get("d.e"), 4)
        pd = PathDict()
        pd.path_set("a.b.c", 1)
        self.assertEqual(pd.path_get("a.b.c"), 1)

    def test_interval_reading(self):
        interval_string = "6h"
        interval = read_update_interval(interval_string)
        self.assertEqual(interval, timedelta(hours=6))
        interval_string = "4h 30m 25s"
        interval = read_update_interval(interval_string)
        self.assertEqual(interval, timedelta(hours=4, minutes=30, seconds=25))
        interval_string = "4w 3d 2s"
        interval = read_update_interval(interval_string)
        self.assertEqual(interval, timedelta(weeks=4, days=3, seconds=2))

    def test_eldritch_names(self):
        for _ in range(100):
            print(generate_random_eldritch_name())

    def test_rewards_string(self):
        print(rewards_string(0, 100, 0))
        print(rewards_string(100, 100, 0))
        print(rewards_string(0, 100, 100))
        print(rewards_string(0, 100, 0, tax=0.5))
