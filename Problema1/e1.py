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
        edges.append((tuple((int(x1),int(y1))),tuple((int(x2),int(y2)))))
    return rows, cols, treasure, UndirectedGraph(E=edges)

    #raise NotImplementedError('read_data')  # Quitar


def df_fromto(g: UndirectedGraph[Vertex], source: Vertex, target: Vertex) -> tuple[list[Vertex], list[Vertex]]:
    def traverse_from(u: Vertex, v: Vertex):
        #para hacer de tesoro a final
        if target not in seen:
            respath.append(v)
        seen.add(v)
        res.append(v)  # Añadimos una arista (recorrido en preorden)
        for suc_v in g.succs(v):
            if suc_v not in seen:
                traverse_from(v, suc_v)
    seen: set[Vertex] = set()
    #usando sets para despues poder hacer diferencias e interseciones
    res: list[Vertex] = list()
    #res: set[Vertex] = set()
    respath: list[Vertex] = []
    #respath: set[Vertex] = set()
    traverse_from(source, source)  # Arista fantasma inicial
    return res, respath

def demolish(g: UndirectedGraph[Vertex], treasure: Vertex, treasurevgroup: list[Vertex]) -> tuple[list[Vertex], Edge]:
    def traverse_wall_to_treasure(u: Vertex, v: Vertex):
        # para hacer de tesoro a final
        nonlocal wall
        if treasure not in seen:
            res.append(v)
        seen.add(v)
        x, y = v
        if wall == (initialpos, initialpos):
            if (x + 1, y) in treasurevgroup:
                wall = (v,(x + 1, y))
                g.add_edge(wall)
                v = wall[1]
                res.append(v)
            elif (x - 1, y) in treasurevgroup:
                wall = (v,(x - 1, y))
                g.add_edge(wall)
                v = wall[1]
                res.append(v)
            elif (x, y + 1) in treasurevgroup:
                wall = (v,(x, y + 1))
                g.add_edge(wall)
                v = wall[1]
                res.append(v)
            elif (x, y - 1) in treasurevgroup:
                wall = (v,(x, y - 1))
                g.add_edge(wall)
                v = wall[1]
                res.append(v)
            seen.add(v)
        for suc_v in g.succs(v):
            if suc_v not in seen:
                traverse_wall_to_treasure(v, suc_v)
    initialpos = (0,0)
    wall: Edge = (initialpos,initialpos)

    res: list[Vertex] = []
    seen: set[Vertex] = set()
    #res: set[Vertex] = set()
    traverse_wall_to_treasure(initialpos, initialpos)
    return res, wall


def process(data: Data) -> Result:
    # TODO: IMPLEMENTAR
    rows, cols, treasure, graph = data
    endpos = rows-1, cols-1
    treasurevgroup, idealpath = df_fromto(graph, treasure, endpos)
    path_hole, wall = demolish(graph, endpos, treasurevgroup)
    print(idealpath)
    print(path_hole)
    #return list(idealpath), wall
    #cambiar sets a list y devolver lista de vertex, no de edges
    # idea para mañana: recorrer desde tesoro a rows-1, cols-1 (final) y crear un camino
    # recorrer desde 0,0  y mirar desde cada vertice la distancia sobre los vertices del camino ya hecho, si = 1 romper pared, entonces acabar recorrido y añadir al camino ya creado lo recorrido desde el inicio+pared rota


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