import argparse
import unittest

import numpy as np

from main import ComplexityCostModel, VolumeCostModel, validate_inputs


class VolumeCostModelTests(unittest.TestCase):
    def test_default_break_even(self) -> None:
        model = VolumeCostModel()
        self.assertAlmostEqual(model.breakeven_volume(), 10.0)

    def test_no_break_even_when_additive_is_cheaper_than_variable_cost(self) -> None:
        model = VolumeCostModel(setup_cost=100.0, variable_cost=20.0, additive_unit_cost=15.0)
        self.assertIsNone(model.breakeven_volume())

    def test_conventional_cost_decreases_with_volume(self) -> None:
        model = VolumeCostModel()
        x = np.array([2.0, 5.0, 20.0, 80.0])
        y = model.conventional_cost(x)
        self.assertTrue(np.all(np.diff(y) < 0))


class ComplexityCostModelTests(unittest.TestCase):
    def test_default_break_even(self) -> None:
        model = ComplexityCostModel()
        expected = (50.0 / 0.1) ** (1 / 2.0)
        self.assertAlmostEqual(model.breakeven_complexity(), expected)

    def test_no_break_even_for_invalid_inputs(self) -> None:
        model = ComplexityCostModel(coefficient=0.0, exponent=2.0, additive_piece_cost=50.0)
        self.assertIsNone(model.breakeven_complexity())


class ValidationTests(unittest.TestCase):
    def test_validate_inputs_rejects_bad_ranges(self) -> None:
        args = argparse.Namespace(max_volume=1.0, max_complexity=10.0, points=500)
        with self.assertRaises(ValueError):
            validate_inputs(args)

        args = argparse.Namespace(max_volume=10.0, max_complexity=1.0, points=500)
        with self.assertRaises(ValueError):
            validate_inputs(args)

        args = argparse.Namespace(max_volume=10.0, max_complexity=10.0, points=5)
        with self.assertRaises(ValueError):
            validate_inputs(args)


if __name__ == "__main__":
    unittest.main()
