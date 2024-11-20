import sys
from dataclasses import dataclass
from typing import TextIO, Iterator, Self

from algoritmia.schemes.bt_scheme import DecisionSequence, bt_solutions, min_solution, bt_vc_solutions

type Data = tuple[int, list[int]]
type Result = list[int] | None

def read_data(f: TextIO) -> Data:
    S = int(f.readline())
    es = list(map(int, f.readlines()))
    return S, es

def process(data: Data) -> Result:
    @dataclass
    class Extra:
        current_sum: int
        num_count: int    # Cantidad de números utilizados en current_sum       # <-------- NUEVO

    class SubsetSumDS(DecisionSequence[int, Extra]):
        def is_solution(self) -> bool:
            return len(self) == len(e) and self.extra.current_sum == S

        def successors(self) -> Iterator[Self]:
            n = len(self)
            if n < len(e):
                yield self.add_decision(0, self.extra)
                new_current_sum = self.extra.current_sum + e[n]
                if new_current_sum <= S:
                    yield self.add_decision(1, Extra(new_current_sum, self.extra.num_count+1))  # <-------- MODIFICADO

        def state(self):
            return len(self), self.extra.current_sum, self.extra.num_count      # <-------- MODIFICADO

    # La función objetivo (la utiliza min_solution)
    def f(decisions: list[int]) -> int:
        return sum(decisions)

    S, e = data
    initial_ds = SubsetSumDS(Extra(0, 0))                                       # <-------- MODIFICADO
    all_solutions = bt_vc_solutions(initial_ds)                                 # <-------- MODIFICADO

    # El enunciado pide la mejor solución o, si no hay ninguna, None
    best_sol = min_solution(all_solutions, f)
    if best_sol is None:
        return None
    _score, sol = best_sol

    # Cambiamos el formato de la solución: de unos y ceros a los elementos del subconjunto
    return [e[i] for i, value in enumerate(sol) if value == 1]

def show_result(result: Result):
    if result is None:
        print('No hay solución')
    else:
        for e in result:
            print(e)


if __name__ == '__main__':
    data0 = read_data(sys.stdin)
    result0 = process(data0)
    show_result(result0)
