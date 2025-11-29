# data_input.py
"""
Moduł do wprowadzania danych (miasta i odległości) dla problemu TSP
"""
def get_example_data():
    # Przykładowa macierz odległości dla 4 miast
    return [
        [0, 10, 15, 20, 30, 10],
        [10, 0, 35, 25, 40, 15],
        [15, 35, 0, 30, 45, 25],
        [20, 25, 30, 0, 50, 35],
        [30, 40, 45, 50, 0, 45],
        [10, 15, 25, 35, 45, 0]
    ]
