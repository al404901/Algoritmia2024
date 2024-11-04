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
from algoritmia.datastructures.queues import Fifo
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
    edges = []
    for line in f.readlines():
        x1, y1, x2, y2 = line.split()
        edges.append((tuple((int(x1),int(y1))),tuple((int(x2),int(y2)))))
    return rows, cols, treasure, UndirectedGraph(E=edges)


def bf_fromtoleft(g: UndirectedGraph[Vertex], source: Vertex, treasurevertex:set[Vertex]) -> tuple[list[Edge], dict[Vertex, Vertex]]:
    distanceside: dict[Vertex, Vertex] = {}
    queue: Fifo[Edge] = Fifo()
    queue.push((source, source))
    seen: set[Vertex] = set()
    seen.add(source)
    res: list[Edge] = list()
    while len(queue) > 0:
        u, v = queue.pop()
        res.append((u,v))
        x, y = v
        if (x + 1, y) in treasurevertex:
            distanceside[(x + 1, y)] = (v)
        if (x, y + 1) in treasurevertex:
            distanceside[(x, y + 1)] = (v)
        if (x, y - 1) in treasurevertex:
            distanceside[(x, y - 1)] = (v)
        for suc in g.succs(v):
            if suc not in seen:
                queue.push((v, suc))
                seen.add(suc)
    return res, distanceside


def bf_fromtoright(g: UndirectedGraph[Vertex], source: Vertex) -> tuple[list[Edge], set[Vertex]]:
    queue: Fifo[Edge] = Fifo()
    queue.push((source, source))
    seen: set[Vertex] = set()
    seen.add(source)
    res: list[Edge] = list()
    while len(queue) > 0:
        u, v = queue.pop()
        res.append((u,v))
        for suc in g.succs(v):
            if suc not in seen:
                queue.push((v, suc))
                seen.add(suc)
    return res, seen


def path_recover(edges: list[Edge], v: Vertex) -> list[Vertex]:
    bp: dict[Vertex, Vertex] = {}
    for o, d in edges:
        bp[d] = o
        if d == v:
            break
    path = [v]
    while v != bp[v]:
        v = bp[v]
        path.append(v)
    path.reverse()
    return path

def path_recover_no_reverse(edges: list[Edge], v: Vertex) -> tuple[list[Vertex], int]:
    bp: dict[Vertex, Vertex] = {}
    counter=0
    for o, d in edges:
        bp[d] = o
        if d == v:
            break
    path = [v]
    while v != bp[v]:
        v = bp[v]
        path.append(v)
        counter+=1
    return path, counter


def process(data: Data) -> Result:
    rows, cols, treasure, graph = data
    endpos = rows-1, cols-1
    right_edges, rightvertex = bf_fromtoright(graph, treasure)
    left_edges, distance_bin=bf_fromtoleft(graph, (0, 0), rightvertex)
    therenomin = True
    treasure_to_end = path_recover(right_edges, endpos)
    for k in distance_bin:
        n= distance_bin[k]
        leftpath, leftlen=path_recover_no_reverse(left_edges, n)
        rightpath, rightlen=path_recover_no_reverse(right_edges, k)
        total_len=leftlen+rightlen
        if therenomin or total_len < minlen:
            minlen = total_len
            therenomin = False
            leftpathmin = leftpath
            rightpathmin = rightpath
            wall=(n, k)
    leftpathmin.reverse()
    treasure_to_end.remove(treasure)
    for vertex in rightpathmin:
        leftpathmin.append(vertex)
    for vertex in treasure_to_end:
        leftpathmin.append(vertex)
    return leftpathmin, wall

# ----- NO MODIFICAR EL PROGRAMA DEBAJO DE ESTA LÍNEA -----

def show_result(result: Result):
    path, edge = result
    print(path)
    print(len(path) - 1)
    print(edge)


# ----- Programa principal -----

if __name__ == '__main__':
    data0 = read_data(sys.stdin)
    result0 = process(data0)
    show_result(result0)