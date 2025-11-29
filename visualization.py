# visualization.py
"""
Moduł do wizualizacji trasy komiwojażera

Używa backendu 'Agg' (headless) i zapisuje wykres do pliku PNG.
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import networkx as nx
import os

def visualize_tsp_route(distance_matrix, route, out_path='tsp_route.png'):
    G = nx.Graph()
    n = len(distance_matrix)
    for i in range(n):
        for j in range(i+1, n):
            G.add_edge(i, j, weight=distance_matrix[i][j])
    pos = nx.circular_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightblue')
    path_edges = [(route[i], route[(i+1)%n]) for i in range(n)]
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2)
    plt.title('Najlepsza trasa TSP')
    plt.tight_layout()
    plt.savefig(out_path)
    print(f'Wizualizacja zapisana jako: {out_path}')
    try:
        # Otwórz plik w systemowym podglądzie (Windows)
        if os.name == 'nt':
            os.startfile(out_path)
    except Exception:
        pass
