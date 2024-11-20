# ==========================================================================================
# IMPORTANTE - Este entregable necesita:
# - Python: versión 3.12 o superior
# - Biblioteca algoritmia: versión 3.1.3 o superior
#   Para instalarla o actualizarla, abre un terminal en PyCharm y ejecuta el comando:
#      pip install algoritmia --upgrade
# ==========================================================================================

import sys
from dataclasses import dataclass
from typing import TextIO, Iterator, Self

# ==========================================================================================
# COMPROBACIÓN DE LAS VERSIONES DE Python Y algoritmia
if sys.version_info < (3, 12):
    print(f"ERROR: Este entregable necesita Python 3.12 o superior (tu versión es la {sys.version_info[0]}.{sys.version_info[1]}).", file=sys.stderr)
    exit(1)
try:
    from algoritmia import TVERSION
    if TVERSION < (3, 1, 3): raise Exception()
except:
    print(f"ERROR: Este entregable necesita la versión 3.1.3 (o superior) de la biblioteca 'algoritmia'.", file=sys.stderr)
    print(f"Abre un terminal de PyCharm y ejecuta la orden:\n\tpip install algoritmia --upgrade", file=sys.stderr)
    exit(1)
# ==========================================================================================

# El esquema de búsqueda con retroceso
from algoritmia.schemes.bt_scheme import DecisionSequence, bt_vc_solutions, max_solution

# Tipos para representar la instancia: ----------------------

type Weight = int
type Value = int
type Item = tuple[Weight, Value]

# Data es el tipo devuelto por la función read_data
# Es la tupla (valor_mínimo, capacidad_mochilas, items)
type Data = tuple[Value, tuple[Weight, Weight], tuple[Item, ...]]

# Tipos para representar el resultado: ----------------------

type Decision = int                                 # 0, 1 o -1 (mira el enunciado)
type Solution = tuple[Value, tuple[Decision, ...]]  # (valor_mochilas, decisiones)

# Result es el tipo devuelto por la función process
# Es la tupla (valor_mochilas, decisiones) o None, si no es posible llegar al mínimo
type Result = Solution | None

# ------------------------------------------------------------------------------------------------

def read_data(f: TextIO) -> Data:
    minValue = int(f.readline())
    aux=f.readline().split()
    backpack_weight=(int(aux[0]), int(aux[1]))
    itemsList=[]
    for remaining_lines in f.readlines():
        aux=remaining_lines.split()
        itemsList.append((int(aux[0]),int(aux[1])))
    items=tuple(itemsList)
    return minValue, backpack_weight, items


def process(data: Data) -> Result:
    @dataclass
    class Extra:
        weight1: int
        weight2: int
        current_value: int

    class DoubleBackpackDS(DecisionSequence[int, Extra]):
        def is_solution(self) -> bool:
            return len(self) == len(items) and self.extra.current_value >= min_value

        def successors(self) -> Iterator[Self]:
            n = len(self)
            if n < len(items):
                weight, value = items[n]
                new_value=value+self.extra.current_value
                new_weight=weight+self.extra.weight1
                if new_weight <= maxWeight1:
                    yield self.add_decision(0, Extra(new_weight, self.extra.weight2, new_value))
                new_weight=weight+self.extra.weight2
                if new_weight <= maxWeight2:
                    yield self.add_decision(1, Extra(self.extra.weight1, new_weight, new_value))
                yield self.add_decision(-1, self.extra)

        def state(self):
            return len(self), self.extra.weight1, self.extra.weight2, self.extra.current_value

    min_value, (maxWeight1, maxWeight2), items = data
    initial_ds = DoubleBackpackDS(Extra(0, 0, 0))
    all_solutions = bt_vc_solutions(initial_ds)
    def f(solution: Solution) -> int:
        return sum(items[i][1] for i, d in enumerate(solution) if d != -1)
    return max_solution(all_solutions, f)

#----- NO MODIFICAR EL PROGRAMA A PARTIR DE ESTA LÍNEA -----

def show_result(result: Result):
    if result is None:
        print('IMPOSSIBLE')
    else:
        s, sol = result
        print(s)
        print(sol)

# ------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    data0 = read_data(sys.stdin)
    result0 = process(data0)
    show_result(result0)