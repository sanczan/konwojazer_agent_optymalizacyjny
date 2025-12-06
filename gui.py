import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import math
from functools import partial

from data_input import MACIERZ_ODLEGLOSCI
from strategies import brute_force, two_opt


def parse_matrix(text):
    lines = [l.strip() for l in text.strip().splitlines() if l.strip()]
    mat = []
    for line in lines:
        """Oddzielenie przecinkiem lub spacją"""
        if ',' in line:
            parts = [p.strip() for p in line.split(',') if p.strip()]
        else:
            parts = [p for p in line.split() if p]
        try:
            row = [float(p) for p in parts]
        except ValueError:
            raise ValueError('Nieprawidłowa liczba w macierzy')
        mat.append(row)
    # validate square
    n = len(mat)
    for r in mat:
        if len(r) != n:
            raise ValueError('Macierz musi być kwadratowa')
    return [[int(x) for x in row] for row in mat]


def format_matrix(mat):
    return '\n'.join(' '.join(str(int(x)) for x in row) for row in mat)


def factorial(n):
    return math.factorial(n)


def brute_force_generator(macierz):
    from itertools import permutations
    n = len(macierz)
    total = factorial(n)
    best_trasa = None
    best_koszt = float('inf')

    for idx, trasa in enumerate(permutations(range(n)), start=1):
        koszt = 0
        for i in range(n):
            od = trasa[i]
            do = trasa[(i + 1) % n]
            koszt += macierz[od][do]

        if koszt < best_koszt:
            best_koszt = koszt
            best_trasa = list(trasa)

        yield {
            'current_trasa': list(trasa),
            'current_koszt': koszt,
            'best_trasa': best_trasa,
            'best_koszt': best_koszt,
            'idx': idx,
            'total': total
        }


def two_opt_generator(macierz):
    n = len(macierz)

    def licz_koszt(trasa):
        koszt = 0
        for i in range(len(trasa)):
            od = trasa[i]
            do = trasa[(i + 1) % len(trasa)]
            koszt += macierz[od][do]
        return koszt

    trasa = list(range(n))
    current_koszt = licz_koszt(trasa)
    yield {
        'stage': 'start',
        'trasa': trasa.copy(),
        'koszt': current_koszt
    }

    improved = True
    """Iteracja dopóki nie będzie poprawy"""
    while improved:
        improved = False
        for i in range(n - 1):
            for j in range(i + 2, n):
                nowa = trasa[:i+1] + trasa[i+1:j+1][::-1] + trasa[j+1:]
                nowy_koszt = licz_koszt(nowa)
                yield {
                    'stage': 'check',
                    'i': i,
                    'j': j,
                    'trasa_proponowana': nowa.copy(),
                    'koszt_proponowany': nowy_koszt,
                    'trasa': trasa.copy(),
                    'koszt': current_koszt
                }

                if nowy_koszt < current_koszt:
                    trasa = nowa
                    current_koszt = nowy_koszt
                    improved = True
                    yield {
                        'stage': 'improve',
                        'i': i,
                        'j': j,
                        'trasa': trasa.copy(),
                        'koszt': current_koszt
                    }
                    break
            if improved:
                break

    yield {
        'stage': 'done',
        'trasa': trasa.copy(),
        'koszt': current_koszt
    }


class TSPGui:
    def __init__(self, root):
        self.root = root
        root.title('Konwojazer - GUI porównawcze')

        """Style"""
        style = ttk.Style()
        try:
            style.theme_use('clam')
        except Exception:
            pass

        """Układ główny"""
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
        root.columnconfigure(2, weight=1)
        root.rowconfigure(0, weight=1)

        """Macierz odległości - lewy panel"""
        frame_left = ttk.Frame(root, padding=8)
        frame_left.grid(row=0, column=0, sticky='nsew')

        ttk.Label(frame_left, text='Macierz odległości (wiersz po wierszu):').grid(row=0, column=0, sticky='w')
        self.text_matrix = scrolledtext.ScrolledText(frame_left, width=36, height=15, font=('Consolas', 10))
        self.text_matrix.grid(row=1, column=0, sticky='nsew', pady=6)
        frame_left.rowconfigure(1, weight=1)
        self.text_matrix.insert('1.0', format_matrix(MACIERZ_ODLEGLOSCI))

        btn_frame = ttk.Frame(frame_left)
        btn_frame.grid(row=2, column=0, sticky='w')
        ttk.Button(btn_frame, text='Wyczyść', command=self.clear_matrix).grid(row=0, column=0, padx=(0,6))
        ttk.Button(btn_frame, text='Wczytaj domyślną', command=self.load_default).grid(row=0, column=1)

        """Środkowy panel: kontrolki i log"""
        frame_center = ttk.Frame(root, padding=8)
        frame_center.grid(row=0, column=1, sticky='nsew')
        frame_center.rowconfigure(2, weight=1)

        """Kontrolki brute-force"""
        ttk.Label(frame_center, text='Brute Force', font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky='w')
        bf_controls = ttk.Frame(frame_center)
        bf_controls.grid(row=1, column=0, sticky='w', pady=4)
        ttk.Button(bf_controls, text='Start', command=self.run_bf_full).grid(row=0, column=0)
        ttk.Button(bf_controls, text='Krok', command=self.run_bf_step).grid(row=0, column=1, padx=6)
        ttk.Button(bf_controls, text='Reset', command=self.reset_bf).grid(row=0, column=2)
        ttk.Button(bf_controls, text='Stop', command=self.stop_bf).grid(row=0, column=3, padx=(6,0))

        """Suwak prędkości brute-force"""
        ttk.Label(bf_controls, text='Prędkość BF:').grid(row=1, column=0, sticky='w', pady=(6,0))
        self.bf_speed_scale = ttk.Scale(bf_controls, from_=1, to=200, orient='horizontal')
        self.bf_speed_scale.set(50)
        self.bf_speed_scale.grid(row=1, column=1, columnspan=3, sticky='we', padx=(6,0), pady=(6,0))

        """Kontrolki agenta (2-opt)"""
        ttk.Label(frame_center, text='Agent (2-Opt)', font=('Segoe UI', 10, 'bold')).grid(row=3, column=0, sticky='w', pady=(8,0))
        ag_controls = ttk.Frame(frame_center)
        ag_controls.grid(row=4, column=0, sticky='w', pady=4)
        ttk.Button(ag_controls, text='Start', command=self.run_agent_full).grid(row=0, column=0)
        ttk.Button(ag_controls, text='Krok', command=self.run_agent_step).grid(row=0, column=1, padx=6)
        ttk.Button(ag_controls, text='Reset', command=self.reset_agent).grid(row=0, column=2)
        ttk.Button(ag_controls, text='Stop', command=self.stop_agent).grid(row=0, column=3, padx=(6,0))

        """Suwak prędkości agenta"""
        ttk.Label(ag_controls, text='Prędkość agenta:').grid(row=1, column=0, sticky='w', pady=(6,0))
        self.agent_speed_scale = ttk.Scale(ag_controls, from_=1, to=500, orient='horizontal')
        self.agent_speed_scale.set(200)
        self.agent_speed_scale.grid(row=1, column=1, columnspan=3, sticky='we', padx=(6,0), pady=(6,0))

        """Obszar logów"""
        ttk.Label(frame_center, text='Log / Wyniki', font=('Segoe UI', 10, 'bold')).grid(row=2, column=0, sticky='w', pady=(8,0))
        self.log = scrolledtext.ScrolledText(frame_center, width=60, height=12, font=('Consolas', 10))
        self.log.grid(row=6, column=0, sticky='nsew', pady=6)

        """Prawy panel: Canvas do wizualizacji"""
        frame_right = ttk.Frame(root, padding=8)
        frame_right.grid(row=0, column=2, sticky='nsew')
        frame_right.rowconfigure(1, weight=1)
        ttk.Label(frame_right, text='Wizualizacja trasy', font=('Segoe UI', 10, 'bold')).grid(row=0, column=0, sticky='w')
        self.canvas = tk.Canvas(frame_right, bg='#ffffff')
        self.canvas.grid(row=1, column=0, sticky='nsew', pady=6)

        """Pasek stanu"""
        self.status = ttk.Label(root, text='Gotowy', relief='sunken', anchor='w')
        self.status.grid(row=1, column=0, columnspan=3, sticky='ew')

        """Stan generatorów"""
        self.bf_gen = None
        self.agent_gen = None
        self.bf_running = False
        self.agent_running = False
        self.current_coords = []

    def clear_matrix(self):
        self.text_matrix.delete('1.0', tk.END)

    def load_default(self):
        self.text_matrix.delete('1.0', tk.END)
        self.text_matrix.insert('1.0', format_matrix(MACIERZ_ODLEGLOSCI))

    def append_log(self, text):
        self.log.insert(tk.END, text + '\n')
        self.log.see(tk.END)
        self.status.config(text=text)

    def reset_bf(self):
        self.bf_gen = None
        self.bf_running = False
        self.append_log('Brute-force: zresetowano')

    def stop_bf(self):
        """Zatrzymanie działającej pętli brute-force bez resetowania generatora"""
        if self.bf_running:
            self.bf_running = False
            self.append_log('Brute-force: zatrzymano')
        else:
            self.append_log('Brute-force: nie było uruchomione')

    def reset_agent(self):
        self.agent_gen = None
        self.agent_running = False
        self.append_log('Agent: zresetowano')

    def stop_agent(self):
        """Zatrzymanie działającej pętli agenta bez resetowania generatora"""
        if self.agent_running:
            self.agent_running = False
            self.append_log('Agent: zatrzymano')
        else:
            self.append_log('Agent: nie było uruchomione')

    def _get_matrix_or_alert(self):
        txt = self.text_matrix.get('1.0', tk.END)
        try:
            mat = parse_matrix(txt)
            if len(mat) > 10:
                if not messagebox.askyesno('Uwaga', 'Liczba miast większa niż 10 — brute-force może być bardzo powolny. Kontynuować?'):
                    return None
            return mat
        except Exception as e:
            messagebox.showerror('Błąd', str(e))
            return None

    """Krok / pełne wykonanie brute-force"""
    def run_bf_step(self):
        mat = self._get_matrix_or_alert()
        if mat is None:
            return

        if self.bf_gen is None:
            self.bf_gen = brute_force_generator(mat)
            self.append_log('Brute-force: rozpoczęto generator kroków')

        try:
            state = next(self.bf_gen)
            """Zapamiętaj najlepszą trasę do końcowej wizualizacji"""
            self.bf_last_best_trasa = state.get('best_trasa')
            self.bf_last_best_koszt = state.get('best_koszt')
            self.append_log(f"Permutacja {state['idx']}/{state['total']}: trasa={state['current_trasa']} koszt={state['current_koszt']} | najlepsza={state['best_trasa']} koszt={state['best_koszt']}")
        except StopIteration:
            self.append_log('Brute-force: koniec')
            """Narysuj ostateczną najlepszą trasę, jeśli dostępna"""
            if getattr(self, 'bf_last_best_trasa', None):
                try:
                    n = len(self.bf_last_best_trasa)
                except Exception:
                    n = 0
                self._draw_final_route(n, self.bf_last_best_trasa)
                self.append_log(f"Brute-force - najlepsza trasa: {self.bf_last_best_trasa} koszt={getattr(self,'bf_last_best_koszt', None)}")
            self.bf_gen = None

    def _bf_step_loop(self):
        if not self.bf_running:
            return
        try:
            state = next(self.bf_gen)
            """Zapamiętaj najlepszą trasę do końcowej wizualizacji"""
            self.bf_last_best_trasa = state.get('best_trasa')
            self.bf_last_best_koszt = state.get('best_koszt')
            self.append_log(f"Permutacja {state['idx']}/{state['total']}: trasa={state['current_trasa']} koszt={state['current_koszt']} | najlepsza={state['best_trasa']} koszt={state['best_koszt']}")
            """Aktualizacja wizualizacji (pokaż aktualną i najlepszą)"""
            try:
                n = len(state['current_trasa'])
            except Exception:
                n = 0
            self._draw_routes(n, state.get('current_trasa'), state.get('best_trasa'))
            """Zaplanuj następny krok z kontrolą prędkości specyficzną dla brute-force"""
            delay = int(max(1, 201 - getattr(self, 'bf_speed_scale').get()))
            self.root.after(delay, self._bf_step_loop)
        except StopIteration:
            self.append_log('Brute-force: koniec')
            """Narysuj ostateczną najlepszą trasę, jeśli dostępna"""
            if getattr(self, 'bf_last_best_trasa', None):
                try:
                    n = len(self.bf_last_best_trasa)
                except Exception:
                    n = 0
                self._draw_final_route(n, self.bf_last_best_trasa)
                self.append_log(f"Brute-force - najlepsza trasa: {self.bf_last_best_trasa} koszt={getattr(self,'bf_last_best_koszt', None)}")
            self.bf_gen = None
            self.bf_running = False

    def run_bf_full(self):
        mat = self._get_matrix_or_alert()
        if mat is None:
            return

        if self.bf_gen is None:
            self.bf_gen = brute_force_generator(mat)
            self.append_log('Brute-force: rozpoczęto pełne wykonanie')

        if self.bf_running:
            return
        self.bf_running = True
        self._bf_step_loop()

    """Krok / pełne wykonanie agenta (two-opt)"""
    def run_agent_step(self):
        mat = self._get_matrix_or_alert()
        if mat is None:
            return

        if self.agent_gen is None:
            self.agent_gen = two_opt_generator(mat)
            self.append_log('Agent (2-opt): rozpoczęto generator kroków')

        try:
            state = next(self.agent_gen)
            self._display_agent_state(state)
        except StopIteration:
            self.append_log('Agent: koniec')
            self.agent_gen = None

    def _display_agent_state(self, state):
        st = state.get('stage')
        if st == 'start':
            self.append_log(f"Agent start: trasa={state['trasa']} koszt={state['koszt']}")
            self._draw_routes(len(state['trasa']), state.get('trasa'))
        elif st == 'check':
            self.append_log(f"Sprawdzanie i={state['i']} j={state['j']}: proponowana={state['trasa_proponowana']} koszt={state['koszt_proponowany']} (aktualna={state['trasa']} koszt={state['koszt']})")
            """Pokaż bieżącą i proponowaną trasę"""
            self._draw_routes(len(state['trasa']), state.get('trasa'), state.get('trasa_proponowana'))
        elif st == 'improve':
            self.append_log(f"POPRAWA! i={state['i']} j={state['j']}: nowa trasa={state['trasa']} koszt={state['koszt']}")
            """Zaktualizuj wizualizację po poprawie"""
            self._draw_routes(len(state['trasa']), state.get('trasa'))
        elif st == 'done':
            self.append_log(f"Agent zakończył: trasa={state['trasa']} koszt={state['koszt']}")
            """Narysuj końcową wyróżnioną trasę"""
            try:
                n = len(state['trasa'])
            except Exception:
                n = 0
            self._draw_final_route(n, state['trasa'])
        else:
            self.append_log(str(state))

    def _compute_coords(self, n):
        """Rozmieszcz punktów na okręgu wewnątrz canvasa"""
        w = max(300, self.canvas.winfo_width() or 400)
        h = max(300, self.canvas.winfo_height() or 400)
        cx, cy = w // 2, h // 2
        r = int(min(w, h) * 0.38)
        coords = []
        for i in range(n):
            ang = 2 * math.pi * i / n - math.pi / 2
            x = cx + int(r * math.cos(ang))
            y = cy + int(r * math.sin(ang))
            coords.append((x, y))
        return coords

    def _draw_routes(self, n, current=None, best=None):
        """Oblicz współrzędne punktów"""
        self.canvas.delete('all')
        if n <= 0:
            return
        coords = self._compute_coords(n)
        self.current_coords = coords

        """Rysuj wierzchołki"""
        for i, (x, y) in enumerate(coords):
            self.canvas.create_oval(x-6, y-6, x+6, y+6, fill='#2a9d8f', outline='')
            self.canvas.create_text(x, y-14, text=str(i), font=('Segoe UI', 9), fill='#264653')

        def draw_line(route, color, width=2, dash=None):
            if not route:
                return
            pts = []
            for idx in route:
                pts.extend(coords[idx])
            """Domknięcie pętli przez dodanie pierwszego punktu"""
            pts.extend(coords[route[0]])
            for i in range(0, len(pts)-2, 2):
                self.canvas.create_line(pts[i], pts[i+1], pts[i+2], pts[i+3], fill=color, width=width, dash=dash)

        """Rysuj najlepszą trasę na niebiesko"""
        draw_line(best, '#1d4ed8', width=3)
        """Narysuj bieżącą trasę jako pomarańczową przerywaną"""
        draw_line(current, '#f97316', width=2, dash=(4, 4))

    def _draw_final_route(self, n, route, color='#16a34a'):
        """Narysuj końcową wyróżnioną trasę (ciągła, grubsza)"""
        self.canvas.delete('all')
        if not route or n <= 0:
            return
        coords = self._compute_coords(n)

        """Rysuj wierzchołki"""
        for i, (x, y) in enumerate(coords):
            self.canvas.create_oval(x-6, y-6, x+6, y+6, fill='#2a9d8f', outline='')
            self.canvas.create_text(x, y-14, text=str(i), font=('Segoe UI', 9), fill='#264653')

        pts = []
        for idx in route:
            pts.extend(coords[idx])
        pts.extend(coords[route[0]])
        for i in range(0, len(pts)-2, 2):
            self.canvas.create_line(pts[i], pts[i+1], pts[i+2], pts[i+3], fill=color, width=4)

    def _agent_step_loop(self):
        if not self.agent_running:
            return
        try:
            state = next(self.agent_gen)
            self._display_agent_state(state)
            """Zaplanuj następny krok z kontrolą prędkości specyficzną dla agenta"""
            delay = int(max(1, 501 - self.agent_speed_scale.get()))
            self.root.after(delay, self._agent_step_loop)
        except StopIteration:
            self.append_log('Agent: koniec')
            self.agent_gen = None
            self.agent_running = False

    def run_agent_full(self):
        mat = self._get_matrix_or_alert()
        if mat is None:
            return

        if self.agent_gen is None:
            self.agent_gen = two_opt_generator(mat)
            self.append_log('Agent (2-opt): rozpoczęto pełne wykonanie')

        if self.agent_running:
            return
        self.agent_running = True
        self._agent_step_loop()


def main():
    root = tk.Tk()
    app = TSPGui(root)
    root.mainloop()


if __name__ == '__main__':
    main()
