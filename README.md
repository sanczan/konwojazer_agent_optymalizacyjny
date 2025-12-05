# System Agentowy - Problem Komiwojażera (TSP)

Prosty system agentowy do rozwiązywania problemu komiwojażera (Traveling Salesman Problem).

## Co to jest?

Program, który używa **agenta** do znajdowania najkrótszej trasy między miastami.

### Agent ma trzy cechy:
- **Autonomiczność** - sam podejmuje decyzje
- **Reaktywność** - reaguje na środowisko (czyta dane)
- **Proaktywność** - dąży do celu (szuka najlepszej trasy)

### Środowisko ma cztery cechy:
- **Dostępne** - agent zna wszystkie odległości
- **Deterministyczne** - odległości się nie zmieniają
- **Epizodyczne** - każde rozwiązanie to osobny epizod
- **Statyczne** - dane nie zmieniają się w trakcie

## Jak to działa?

Agent pracuje w pętli:
1. **Percepcja** - odbiera dane ze środowiska
2. **Decyzja** - decyduje co zrobić
3. **Akcja** - wykonuje optymalizację

## Strategie optymalizacji

### 1. Brute Force (siłowa)
- Sprawdza **wszystkie** możliwe trasy
- Zawsze znajdzie najlepsze rozwiązanie
- Działa wolno dla wielu miast (więcej niż ~10)

### 2. 2-Opt
- Poprawia trasę zamieniając krawędzie
- Działa szybko nawet dla wielu miast
- Znajduje dobre (ale nie zawsze najlepsze) rozwiązanie

## Pliki w projekcie

- `agent.py` - klasa agenta
- `strategies.py` - algorytmy optymalizacji
- `data_input.py` - dane wejściowe (macierz odległości)
- `main.py` - główny program

## Jak uruchomić?

```bash
python main.py
```

## Jak zmienić dane?

Edytuj plik `data_input.py` i zmień macierz `MACIERZ_ODLEGLOSCI`.

Przykład dla 4 miast:
```python
MACIERZ_ODLEGLOSCI = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]
```

## Wymagania

Tylko Python 3! Nie trzeba instalować żadnych bibliotek.
