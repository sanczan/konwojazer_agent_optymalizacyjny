# strategies.py
"""
Proste strategie optymalizacyjne dla TSP
"""
from itertools import permutations

def brute_force(macierz):
    """
    Metoda siłowa - sprawdza wszystkie możliwe trasy
    Działa dobrze dla małej liczby miast (do ~10)
    """
    n = len(macierz)
    miasta = list(range(n))
    
    najlepsza_trasa = None
    najlepszy_koszt = float('inf')
    
    # Sprawdzamy wszystkie permutacje
    for trasa in permutations(miasta):
        # Liczymy koszt tej trasy
        koszt = 0
        for i in range(n):
            od = trasa[i]
            do = trasa[(i + 1) % n]  # powrót do startu
            koszt += macierz[od][do]
        
        # Czy to najlepsza trasa?
        if koszt < najlepszy_koszt:
            najlepszy_koszt = koszt
            najlepsza_trasa = trasa
    
    return list(najlepsza_trasa), najlepszy_koszt


def two_opt(macierz):
    """
    Algorytm 2-opt - zamienia krawędzie w trasie
    Działa dla większej liczby miast
    """
    n = len(macierz)
    
    # Startujemy z prostą trasą 0->1->2->...->n-1->0
    trasa = list(range(n))
    
    def licz_koszt(trasa):
        koszt = 0
        for i in range(len(trasa)):
            od = trasa[i]
            do = trasa[(i + 1) % len(trasa)]
            koszt += macierz[od][do]
        return koszt
    
    poprawiono = True
    
    # Próbujemy poprawiać trasę
    while poprawiono:
        poprawiono = False
        
        # Sprawdzamy wszystkie pary krawędzi
        for i in range(n - 1):
            for j in range(i + 2, n):
                # Próbujemy odwrócić fragment trasy
                nowa_trasa = trasa[:i+1] + trasa[i+1:j+1][::-1] + trasa[j+1:]
                
                # Czy jest lepiej?
                if licz_koszt(nowa_trasa) < licz_koszt(trasa):
                    trasa = nowa_trasa
                    poprawiono = True
                    break
            
            if poprawiono:
                break
    
    return trasa, licz_koszt(trasa)


# Słownik strategii
STRATEGIE = {
    'brute_force': brute_force,
    'two_opt': two_opt
}
