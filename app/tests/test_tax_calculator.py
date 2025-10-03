import unittest

from src.use_cases.trade_tax_calculator import calculate_taxes


class MyTestCase(unittest.TestCase):

    def test_case_1_tax_exempt_under_20000(self):
        operations = [
            {"operation": "buy", "unit-cost": 10.00, "quantity": 100},
            {"operation": "sell", "unit-cost": 15.00, "quantity": 50},
            {"operation": "sell", "unit-cost": 15.00, "quantity": 50}
        ]
        expected = [{"tax": 0.0}, {"tax": 0.0}, {"tax": 0.0}]
        self.assertEqual(calculate_taxes(operations), expected)

    def test_case_3_loss_offset_applied_to_profit(self):
        operations = [
            {"operation": "buy", "unit-cost": 10.00, "quantity": 10000},
            {"operation": "sell", "unit-cost": 5.00, "quantity": 5000},
            {"operation": "sell", "unit-cost": 20.00, "quantity": 3000}
        ]
        expected = [{"tax": 0.0}, {"tax": 0.0}, {"tax": 1000.0}]
        self.assertEqual(calculate_taxes(operations), expected)

    def test_case_4_weighted_average_no_profit(self):
        operations = [
            {"operation": "buy", "unit-cost": 10.00, "quantity": 10000},
            {"operation": "buy", "unit-cost": 25.00, "quantity": 5000},
            {"operation": "sell", "unit-cost": 15.00, "quantity": 10000}
        ]
        expected = [{"tax": 0.0}, {"tax": 0.0}, {"tax": 0.0}]
        self.assertEqual(calculate_taxes(operations), expected)

    def test_case_5_weighted_average_with_profit(self):
        operations = [
            {"operation": "buy", "unit-cost": 10.00, "quantity": 10000},
            {"operation": "buy", "unit-cost": 25.00, "quantity": 5000},
            {"operation": "sell", "unit-cost": 15.00, "quantity": 10000},
            {"operation": "sell", "unit-cost": 25.00, "quantity": 5000}
        ]
        expected = [{"tax": 0.0}, {"tax": 0.0}, {"tax": 0.0}, {"tax": 10000.0}]
        self.assertEqual(calculate_taxes(operations), expected)

    def test_case_6_loss_carryforward_and_tax_on_remaining_profit(self):
        operations = [
            {"operation": "buy", "unit-cost": 10.00, "quantity": 10000},
            {"operation": "sell", "unit-cost": 2.00, "quantity": 5000},
            {"operation": "sell", "unit-cost": 20.00, "quantity": 2000},
            {"operation": "sell", "unit-cost": 20.00, "quantity": 2000},
            {"operation": "sell", "unit-cost": 25.00, "quantity": 1000}
        ]
        expected = [
            {"tax": 0.0},
            {"tax": 0.0},
            {"tax": 0.0},
            {"tax": 0.0},
            {"tax": 3000.0}
        ]
        self.assertEqual(calculate_taxes(operations), expected)

    def test_case_7_complex_loss_and_profit_sequence(self):
        operations = [
            {"operation": "buy", "unit-cost": 10.00, "quantity": 10000},
            {"operation": "sell", "unit-cost": 2.00, "quantity": 5000},
            {"operation": "sell", "unit-cost": 20.00, "quantity": 2000},
            {"operation": "sell", "unit-cost": 20.00, "quantity": 2000},
            {"operation": "sell", "unit-cost": 25.00, "quantity": 1000},
            {"operation": "buy", "unit-cost": 20.00, "quantity": 10000},
            {"operation": "sell", "unit-cost": 15.00, "quantity": 5000},
            {"operation": "sell", "unit-cost": 30.00, "quantity": 4350},
            {"operation": "sell", "unit-cost": 30.00, "quantity": 650}
        ]
        expected = [
            {"tax": 0.0},
            {"tax": 0.0},
            {"tax": 0.0},
            {"tax": 0.0},
            {"tax": 3000.0},
            {"tax": 0.0},
            {"tax": 0.0},
            {"tax": 3700.0},
            {"tax": 0.0}
        ]
        self.assertEqual(calculate_taxes(operations), expected)

    def test_case_8_high_profit_tax_applied(self):
        operations = [
            {"operation": "buy", "unit-cost": 10.00, "quantity": 10000},
            {"operation": "sell", "unit-cost": 50.00, "quantity": 10000},
            {"operation": "buy", "unit-cost": 20.00, "quantity": 10000},
            {"operation": "sell", "unit-cost": 50.00, "quantity": 10000}
        ]
        expected = [
            {"tax": 0.0},
            {"tax": 80000.0},
            {"tax": 0.0},
            {"tax": 60000.0}
        ]
        self.assertEqual(calculate_taxes(operations), expected)

    def test_case_9_loss_accumulation_and_partial_deduction(self):
        operations = [
            {"operation": "buy", "unit-cost": 5000.00, "quantity": 10},
            {"operation": "sell", "unit-cost": 4000.00, "quantity": 5},
            {"operation": "buy", "unit-cost": 15000.00, "quantity": 5},
            {"operation": "buy", "unit-cost": 4000.00, "quantity": 2},
            {"operation": "buy", "unit-cost": 23000.00, "quantity": 2},
            {"operation": "sell", "unit-cost": 20000.00, "quantity": 1},
            {"operation": "sell", "unit-cost": 12000.00, "quantity": 10},
            {"operation": "sell", "unit-cost": 15000.00, "quantity": 3}
        ]
        expected = [
            {"tax": 0.0},
            {"tax": 0.0},
            {"tax": 0.0},
            {"tax": 0.0},
            {"tax": 0.0},
            {"tax": 0.0},
            {"tax": 1000.0},
            {"tax": 2400.0}
        ]
        self.assertEqual(calculate_taxes(operations),  expected)
