# main.py
"""
Agent optymalizacyjny do rozwiązywania problemu komiwojażera (TSP)
"""

from data_input import get_example_data
from tsp_solver import solve_tsp_brute_force
from visualization import visualize_tsp_route

def main():
    print("Agent TSP - start")
    distance_matrix = get_example_data()
    route, cost = solve_tsp_brute_force(distance_matrix)
    print(f'Najlepsza trasa: {route}, koszt: {cost}')
    visualize_tsp_route(distance_matrix, route)

if __name__ == "__main__":
    main()
