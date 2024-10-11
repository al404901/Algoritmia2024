# ==========================================================================================
# IMPORTANTE - Este entregable necesita:
# - Python: versión 3.12 o superior
# - Biblioteca algoritmia: versión 3.1.3 o superior
#   Para instalarla o actualizarla, abre un terminal en PyCharm y ejecuta el comando:
#      pip install algoritmia --upgrade
# ==========================================================================================

import sys
from copy import deepcopy
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
    edges = []
    for line in f.readlines():
        x1, y1, x2, y2 = line.split()
        edges.append((tuple((int(x1),int(y1))),tuple((int(x2),int(y2)))))
    return rows, cols, treasure, UndirectedGraph(E=edges)

    #raise NotImplementedError('read_data')  # Quitar


def df_fromto(g: UndirectedGraph[Vertex], source: Vertex) -> tuple[list[Edge], set[Vertex]]:
    def traverse_from(u: Vertex, v: Vertex):
        #if target not in seen:
            #respath.append((u, v))
        seen.add(v)
        res.append((u,v))
        for suc_v in g.succs(v):
            if suc_v not in seen:
                traverse_from(v, suc_v)
    seen: set[Vertex] = set()
    res: list[Edge] = list()
    traverse_from(source, source)  # Arista fantasma inicial
    return res, seen


def wall_list(g: UndirectedGraph[Vertex], treasurevertex: set[Vertex]) -> list[Edge]:
    def traverse_from(u: Vertex, v: Vertex):
        seen.add(v)
        x, y = v
        if (x + 1, y) in treasurevertex:
            wall = (v, (x + 1, y))
            res.append(wall)
        if (x - 1, y) in treasurevertex:
            wall = (v, (x - 1, y))
            res.append(wall)
        if (x, y + 1) in treasurevertex:
            wall = (v, (x, y + 1))
            res.append(wall)
        if (x, y - 1) in treasurevertex:
            wall = (v, (x, y - 1))
            res.append(wall)
        for suc_v in g.succs(v):
            if suc_v not in seen:
                traverse_from(v, suc_v)
    initialpos = (0, 0)
    seen: set[Vertex] = set()
    res: list[Edge] = list()
    traverse_from(initialpos, initialpos)  # Arista fantasma inicial
    return res


def path_recover(edges: list[Edge], v: Vertex) -> list[Vertex]:
    # Creates backpointer dictionary (bp)
    bp: dict[Vertex, Vertex] = {}
    for o, d in edges:
        bp[d] = o
        if d == v: # I have all I need
            break
    # Recover the path jumping back
    path = [v]
    while v != bp[v]:
        v = bp[v]
        path.append(v)
    # reverse the path
    path.reverse()
    return path

#def demolish(g: UndirectedGraph[Vertex], treasure: Vertex, treasurevgroup: list[Vertex]) -> tuple[list[Vertex], Edge]:
    #def traverse_start_to_treasure(v: Vertex, u: Vertex):
   # initialpos = (0,0)
    #wall: Edge = (initialpos,initialpos)
    #res: list[Vertex] = []
    #seen: set[Vertex] = set()
    #traverse_start_to_treasure(initialpos, initialpos)
    #return res, wall


def process(data: Data) -> Result:
    # TODO: IMPLEMENTAR
    rows, cols, treasure, graph = data
    endpos = rows-1, cols-1
    treasure_edges, treasurevertex = df_fromto(graph, treasure)
    minlen=999999999999999999999999999
    short_edges: list[Edge] = []
    minwall: Edge
    for wall in wall_list(graph, treasurevertex):
        auxgraph=deepcopy(graph)
        auxgraph.add_edge(wall)
        start_to_treasure=df_fromto(auxgraph, (0, 0))[0]
        if len(start_to_treasure) <= minlen:
            minlen = len(start_to_treasure)
            short_edges = start_to_treasure
            minwall = wall
    graph.add_edge(minwall)
    finalpath=path_recover(short_edges, treasure)
    for vertex in path_recover(treasure_edges, endpos):
        finalpath.append(vertex)
    finalpath.remove(treasure)
    return finalpath, minwall



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
    result0 = process(data0)
    show_result(result0)