import unittest
from generator import Generator
from hitori_exceptions import NoSolution
from solver import Solver


class SolverTestCase(unittest.TestCase):

    hitori_3x3 = [[1, 1, 2], [3, 2, 3], [3, 3, 3]]
    hitori_5x5 = [[4, 5, 4, 5, 5], [5, 1, 3, 5, 2], [4, 4, 3, 3, 1], [1, 5, 2, 1, 4], [3, 3, 3, 2, 5]]
    hitori_5x5_no_solution = [[4, 2, 3, 2, 5], [2, 3, 1, 1, 3], [4, 4, 5, 4, 1], [5, 4, 1, 1, 2], [3, 2, 2, 2, 5]]
    hitori_5x5_22_solution = [[5, 5, 2, 1, 3], [1, 1, 4, 2, 5], [2, 1, 5, 4, 1], [4, 2, 3, 5, 3], [5, 3, 1, 2, 4]]

    def test_has_solution_3x3(self) -> None:
        solver = Solver(self.hitori_3x3, 1)
        solution = solver.solve()
        self.assertIsNotNone(solution)
        self.assertGreater(len(solution), 0)
        self.assertIsNotNone(solution[0])

    def test_has_solution_5x5(self) -> None:
        solver = Solver(self.hitori_5x5, 1)
        solution = solver.solve()
        self.assertIsNotNone(solution)
        self.assertGreater(len(solution), 0)
        self.assertIsNotNone(solution[0])

    def test_raise_if_has_no_solution(self) -> None:
        solver = Solver(self.hitori_5x5_no_solution)
        self.assertRaises(NoSolution, solver.solve)

    def test_find_all_solutions(self) -> None:
        solver = Solver(self.hitori_5x5_22_solution)
        solutions = solver.solve()
        self.assertEqual(len(solutions), 22)

    def test_find_one_solution_instead_of_all(self) -> None:
        solver = Solver(self.hitori_5x5_22_solution, 1)
        solution = solver.solve()
        self.assertEqual(len(solution), 1)

    def test_required_sum(self) -> None:
        solver = Solver(self.hitori_5x5_22_solution, required_sum=10)
        self.assertRaises(NoSolution, solver.solve)
        solver = Solver(self.hitori_5x5_22_solution, required_sum=13)
        solutions = solver.solve()
        self.assertEqual(len(solutions), 10)


class GeneratorTestCase(unittest.TestCase):

    def test_can_generate(self) -> None:
        self.can_generate_helper(3)
        self.can_generate_helper(4)
        self.can_generate_helper(5)
        self.can_generate_helper(6)
        self.can_generate_helper(7)
        self.can_generate_helper(8)

    def test_generating_field_has_solution(self) -> None:
        for i in range(10):
            size = 3 + i % 3
            field = Generator(size).generate()
            solver = Solver(field, 1)
            solution = solver.solve()
            self.assertIsNotNone(solution)
            self.assertGreater(len(solution), 0)
            self.assertIsNotNone(solution[0])

    def can_generate_helper(self, size) -> None:
        hitori_field = Generator(size).generate()
        self.assertIsNotNone(hitori_field)
        sizes = {*map(lambda x: len(x), hitori_field), len(hitori_field)}
        self.assertTrue(len(sizes) == 1)


if __name__ == '__main__':
    unittest.main()
