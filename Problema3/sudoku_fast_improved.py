import sys
from dataclasses import dataclass
from typing import TextIO, Iterator, Self

from sudoku_lib import from_strings, pretty_print, allowed, empty_cells
from algoritmia.schemes.bt_scheme import DecisionSequence, bt_solutions, Solution

type Sudoku = list[list[int]]
type Data = Sudoku
type Result = Iterator[Sudoku]

def read_data(f: TextIO) -> Data:
    return from_strings(f.readlines())

def process(initial_sudoku: Data) -> Result:
    @dataclass
    class Extra:
        sudoku: list[list[int]]
        empty: set[tuple[int, int]]  # Conjunto con las coordenadas de las celdas vacías (con ceros)

    class SudokuDS(DecisionSequence[int, Extra]):
        def solution(self) -> Solution:
            return self.extra.sudoku

        def is_solution(self) -> bool:
            return len(self.extra.empty) == 0

        def successors(self) -> Iterator[Self]:
            if len(self.extra.empty) > 0:
                # Averigura la posición del cero con menos allowed
                best_pos = -1
                best_allowed = 10  # cualquier número mayor que 9 (el nº máximo de allowed posible)
                for pos in self.extra.empty:
                    num_allowed = len(allowed(self.extra.sudoku, pos))
                    if num_allowed < best_allowed:
                        best_allowed = num_allowed
                        best_pos = pos
                # Versión de una línea del código anterior (está comentada por ser bastante más lenta)
                #  _, best_pos = min((len(allowed(self.extra.sudoku, pos)), pos) for pos in self.extra.empty)

                # Modificamos el original
                self.extra.empty.remove(best_pos)
                r, c = best_pos
                for num in allowed(self.extra.sudoku, best_pos):
                    # Modificamos el original
                    self.extra.sudoku[r][c] = num
                    # Generamos un nuevo SudokuDS con un cero menos
                    yield self.add_decision(num, self.extra)
                # Deshacemos los cambios
                self.extra.empty.add(best_pos)
                self.extra.sudoku[r][c] = 0

    ecs = set(empty_cells(initial_sudoku))
    initial_ds = SudokuDS(Extra(initial_sudoku, ecs))
    return bt_solutions(initial_ds)

def show_result(result: Result):
    for s in result:
        pretty_print(s)


if __name__ == '__main__':
    data0 = read_data(sys.stdin)
    result0 = process(data0)
    show_result(result0)