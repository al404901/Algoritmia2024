import sys
from copy import deepcopy
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
                best_allowed = 100
                for pos in self.extra.empty:
                    num_allowed = len(allowed(self.extra.sudoku, pos))
                    if num_allowed < best_allowed:
                        best_allowed = num_allowed
                        best_pos = pos
                # Versión de una línea del código anterior (está comentada por ser bastante más lenta)
                #  _, best_pos = min((len(allowed(self.extra.sudoku, pos)), pos) for pos in self.extra.empty)

                # Copia de self.extra.empy
                new_empty = deepcopy(self.extra.empty)
                # Modificamos la copia
                new_empty.remove(best_pos)
                for num in allowed(self.extra.sudoku, best_pos):
                    # Copia de self.extra.sudoku
                    new_sudoku = deepcopy(self.extra.sudoku)
                    # Modificamos la copia
                    r, c = best_pos
                    new_sudoku[r][c] = num
                    # Generamos un nuevo SudokuDS con un cero menos
                    yield self.add_decision(num, Extra(new_sudoku, new_empty))

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