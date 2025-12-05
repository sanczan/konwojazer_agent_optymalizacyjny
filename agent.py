# agent.py
"""
Prosty agent optymalizacyjny dla problemu TSP

Agent ma cechy:
- Autonomiczność - sam podejmuje decyzje
- Reaktywność - reaguje na środowisko
- Proaktywność - dąży do celu
"""

class Agent:
    """Bazowa klasa agenta"""
    
    def __init__(self, nazwa):
        self.nazwa = nazwa
        self.cel = "znaleźć najlepszą trasę TSP"
        self.przekonania = {}
        
    def percepcja(self, srodowisko):
        """Agent odbiera informacje ze środowiska"""
        self.przekonania = {
            'liczba_miast': len(srodowisko['macierz']),
            'macierz': srodowisko['macierz'],
            'najlepszy_koszt': srodowisko['najlepszy_koszt']
        }
        return self.przekonania
    
    def decyzja(self):
        """Agent decyduje co zrobić"""
        return 'optymalizuj'
    
    def akcja(self, strategia):
        """Agent wykonuje optymalizację"""
        macierz = self.przekonania['macierz']
        trasa, koszt = strategia(macierz)
        return trasa, koszt
    
    def uruchom(self, srodowisko, strategia):
        """Główna pętla: percepcja -> decyzja -> akcja"""
        # 1. Percepcja
        self.percepcja(srodowisko)
        
        # 2. Decyzja
        decyzja = self.decyzja()
        
        # 3. Akcja
        if decyzja == 'optymalizuj':
            trasa, koszt = self.akcja(strategia)
            return trasa, koszt
