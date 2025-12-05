# main.py
"""
Prosty system agentowy do rozwiązywania problemu TSP
"""
from agent import Agent
from strategies import brute_force, two_opt
from data_input import MACIERZ_ODLEGLOSCI

def main():
    print("=" * 60)
    print("Agent optymalizacyjny - Problem Komiwojażera")
    print("=" * 60)
    print()
    
    # Środowisko 
    # Dostępne: TAK (agent zna wszystkie odległości)
    # Deterministyczne: TAK (odległości się nie zmieniają)
    # Epizodyczne: TAK (każde rozwiązanie to osobny epizod)
    # Statyczne: TAK (dane nie zmieniają się)

    srodowisko = {
        'macierz': MACIERZ_ODLEGLOSCI,
        'najlepszy_koszt': float('inf')
    }
    
    print(f"Liczba wierzchołków: {len(MACIERZ_ODLEGLOSCI)}")
    
    # Testujemy dwie strategie
    strategie = [
        ('Brute Force', brute_force),
        ('2-Opt', two_opt)
    ]
    
    wyniki = []
    
    for nazwa_strategii, strategia in strategie:
        print("-" * 60)
        print(f"{nazwa_strategii}\n")
        
        
        # Tworzymy agenta
        agent = Agent(f"Agent-{nazwa_strategii}")
        
        
        # Agent działa: percepcja -> decyzja -> akcja
        # 1. PERCEPCJA - agent odbiera dane ze środowiska
        # 2. DECYZJA - agent decyduje jak optymalizować
        # 3. AKCJA - agent wykonuje optymalizację
        print()
        trasa, koszt = agent.uruchom(srodowisko, strategia)

        # Wynik
        print(f"Trasa: {trasa}")
        print(f"Koszt trasy: {koszt}")
        print()
        
        wyniki.append((nazwa_strategii, trasa, koszt))
        
        # Aktualizujemy środowisko
        if koszt < srodowisko['najlepszy_koszt']:
            srodowisko['najlepszy_koszt'] = koszt
            srodowisko['najlepsza_trasa'] = trasa
    

if __name__ == "__main__":
    main()
