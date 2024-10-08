# ==========================================================================================
# IMPORTANTE - Este entregable necesita:
# - Python: versión 3.12 o superior
# - Biblioteca algoritmia: versión 3.1.3 o superior
#   Para instalarla o actualizarla, abre un terminal en PyCharm y ejecuta el comando:
#      pip install algoritmia --upgrade
# ==========================================================================================

import sys
from typing import TextIO

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

# Añadid los imports de algoritmia que necesitéis aquí debajo:
from algoritmia.datastructures.graphs import UndirectedGraph

# ------ Tipos ------

type Vertex = tuple[int, int]
type Edge = tuple[Vertex, Vertex]
type Path = list[Vertex]            # Un camino es una lista de vértices

# Data es el tipo devuelto por read_data()
# Es la tupla: (num_rows, num_cols, pos_treasure, undirected_graph)
type Data = tuple[int, int, Vertex, UndirectedGraph[Vertex]]

# Result es el tipo devuelto por process()
# Es la tupla: (path, added_edge)
type Result = tuple[Path, Edge]

# ----- Funciones -----

def read_data(f: TextIO) -> Data:
    # TODO: IMPLEMENTAR

    rows, cols = (int(s) for s in f.readline().split())
    treasure = tuple(int(s) for s in f.readline().split())
    vertices = []
    edges = []
    for line in f.readlines():
        x1, y1, x2, y2 = line.split()
        #vertices.append((int(x1), int(y1)))
        #vertices.append((int(x2), int(y2)))
        #edges.append(((int(x2), int(y2))
        #edges.append(((int(x1), int(y1)), (int(x2), int(y2))))
        edges.append((tuple((int(x1),int(y1))),tuple((int(x2),int(y2)))))
        #Solucionar lo de la lista de vertices
    return rows, cols, treasure, UndirectedGraph(E=edges)

    #raise NotImplementedError('read_data')  # Quitar




def df(g: UndirectedGraph[Vertex], source: Vertex, target: Vertex, preorder: bool = True) -> list[Edge]:
    def traverse_from(u: Vertex, v: Vertex):
        seen.add(v)
        if preorder:
            res.append((u, v))  # Añadimos una arista (recorrido en preorden)
        for suc_v in g.succs(v):
            if suc_v not in seen:
                traverse_from(v, suc_v)
        if not preorder:
            res.append((u, v))  # Añadimos una arista (recorrido en postorden)
    seen: set[Vertex] = set()
    res: list[Edge[Vertex]] = []
    traverse_from(source, source)  # Arista fantasma inicial
    return res


def process(data: Data) -> Result:
    # TODO: IMPLEMENTAR
    rows, cols, treasure, graph = data

    #raise NotImplementedError('process')  # Quitar

# ----- NO MODIFICAR EL PROGRAMA DEBAJO DE ESTA LÍNEA -----

def show_result(result: Result):
    path, edge = result
    print(path)
    print(len(path) - 1)
    print(edge)


# ----- Programa principal -----

if __name__ == '__main__':
    data0 = read_data(sys.stdin)
    print(data0)
    result0 = process(data0)
    show_result(result0)