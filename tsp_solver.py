# tsp_solver.py
"""
Moduł z algorytmem rozwiązującym problem komiwojażera (TSP)
"""
import itertools

def solve_tsp_brute_force(distance_matrix):
    n = len(distance_matrix)
    cities = list(range(n))
    min_path = None
    min_cost = float('inf')
    for perm in itertools.permutations(cities):
        cost = sum(distance_matrix[perm[i]][perm[(i+1)%n]] for i in range(n))
        if cost < min_cost:
            min_cost = cost
            min_path = perm
    return min_path, min_cost
