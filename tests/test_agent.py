import unittest
from agent import Agent


def fake_strategy(macierz):
    """Zwraca stałą trasę i koszt dla testów."""
    return list(range(len(macierz))), 42


class TestAgent(unittest.TestCase):
    def test_percepcja_sets_beliefs(self):
        a = Agent('tester')
        env = {'macierz': [[0, 1], [1, 0]], 'najlepszy_koszt': 999}
        beliefs = a.percepcja(env)
        self.assertEqual(beliefs['liczba_miast'], 2)
        self.assertIs(beliefs['macierz'], env['macierz'])
        self.assertEqual(beliefs['najlepszy_koszt'], 999)

    def test_uruchom_calls_strategy_and_returns(self):
        a = Agent('tester')
        env = {'macierz': [[0, 1, 2], [1, 0, 3], [2, 3, 0]], 'najlepszy_koszt': 1000}
        route, cost = a.uruchom(env, fake_strategy)
        self.assertEqual(cost, 42)
        self.assertEqual(route, [0, 1, 2])


if __name__ == '__main__':
    unittest.main()
