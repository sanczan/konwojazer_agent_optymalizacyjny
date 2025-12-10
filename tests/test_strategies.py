import unittest
from strategies import brute_force


def is_cycle_equivalent(route, target):
    if len(route) != len(target):
        return False
    n = len(route)
    """Sprawdza, czy `route` jest równoważna cyklicznie do `target` (w dowolnym obrocie lub odwrócona)."""
    for shift in range(n):
        if route == target[shift:] + target[:shift]:
            return True
    # check reversed rotations
    rev = target[::-1]
    for shift in range(n):
        if route == rev[shift:] + rev[:shift]:
            return True
    return False


class TestStrategies(unittest.TestCase):
    def test_brute_force_small(self):
        """Testuje algorytm brute_force na małej macierzy kosztów."""
        mat = [
            [0, 1, 10, 1],
            [1, 0, 1, 10],
            [10, 1, 0, 1],
            [1, 10, 1, 0]
        ]

        best_route, best_cost = brute_force(mat)

        self.assertEqual(best_cost, 4)
        self.assertTrue(is_cycle_equivalent(best_route, [0, 1, 2, 3]))


if __name__ == '__main__':
    unittest.main()
