import sys
from copy import deepcopy
from dataclasses import dataclass
from typing import TextIO, Iterator, Self

from sudoku_lib import from_strings, pretty_print, first_empty, allowed
from algoritmia.schemes.bt_scheme import DecisionSequence, bt_solutions

type Sudoku = list[list[int]]
type Data = Sudoku
type Result = Iterator[Sudoku]
type Decision = int
type Solution = Sudoku

def read_data(f: TextIO) -> Data:
    return from_strings(f.readlines())

def process(initial_sudoku: Data) -> Result:
    @dataclass
    class Extra:
        sudoku: list[list[int]]

    class SudokuDS(DecisionSequence[Decision, Extra]):
        def solution(self) -> Solution:
            return self.extra.sudoku

        def is_solution(self) -> bool:
            return first_empty(self.extra.sudoku) is None

        def successors(self) -> Iterator[Self]:
            pos = first_empty(self.extra.sudoku)
            if pos is not None:
                for num in allowed(self.extra.sudoku, pos):
                    # Copia de self.extra.sudoku
                    new_sudoku = deepcopy(self.extra.sudoku)
                    # Modificamos la copia
                    r, c = pos
                    new_sudoku[r][c] = num
                    # Generamos un nuevo SudokuDS con un cero menos
                    yield self.add_decision(num, Extra(new_sudoku))

    initial_ds = SudokuDS(Extra(initial_sudoku))
    return bt_solutions(initial_ds)

def show_result(result: Result):
    for s in result:
        pretty_print(s)


if __name__ == '__main__':
    data0 = read_data(sys.stdin)
    result0 = process(data0)
    show_result(result0)