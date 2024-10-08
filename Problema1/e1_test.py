# Version 1.1 (2024-10-07). Mejora los mensajes de error

import os
import sys
from glob import glob
from time import process_time
from io import StringIO

# ==========================================================================================
# COMPROBACIÓN DE LAS VERSIONES DE Python Y algoritmia
if sys.version_info < (3, 12):
    print(f"ERROR: Este entregable necesita Python 3.12 o superior (tu versión es la {sys.version_info[0]}.{sys.version_info[1]}).", file=sys.stderr)
    exit(1)
try:
    from algoritmia import TVERSION
    if TVERSION < (3, 1, 3): raise Exception()
except:
    print(f"ERROR: Este entregable necesita la versión 3.1.3 de la biblioteca 'algoritmia'.", file=sys.stderr)
    print(f"Abre un terminal de PyCharm y ejecuta la orden:\n\tpip install algoritmia --upgrade", file=sys.stderr)
    exit(1)
# ==========================================================================================

from algoritmia.datastructures.graphs import UndirectedGraph

from e1 import read_data, process, Data, Result, Vertex, Edge, Path

def check_added_edge(g_orig: UndirectedGraph[Vertex], added_edge: Edge) -> list[str]:
    added_edge_errors = []
    u, v = added_edge
    if u in g_orig.succs(v):
        added_edge_errors.append(f"La arista añadida, {added_edge}, ya existía en el grafo.")
    else:
        ur, uc = u
        vr, vc = v
        if u in g_orig.V and v in g_orig.V and ur == vr and abs(uc - vc) == 1 or uc == vc and abs(ur - vr) == 1:
            pass
        else:
            added_edge_errors.append(f"La arista añadida, {added_edge}, no es válida: no conecta celdas vecinas.")
    return added_edge_errors

def check_path(num_rows: int, num_cols: int, treasure_pos: Vertex,
               g_orig: UndirectedGraph[Vertex], path: Path) -> list[str]:
    path_errors = []

    # Error en path ------
    if path[0] != (0, 0):
        path_errors.append(f"El camino no parte de la celda (0, 0).")
    if path[-1] != (num_rows - 1, num_cols - 1):
        path_errors.append(f"El camino no termina en la celda {(num_rows - 1, num_cols - 1)}.")

    u = path[0]
    treasure_picked = False
    for v in path[1:]:
        if v == treasure_pos:
            treasure_picked = True
        if v not in g_orig.succs(u):
            path_errors.append(f"El camino no es válido: no existe la arista entre los vértices {u} y {v}.")
            break
        u = v
    else:
        if not treasure_picked:
            path_errors.append(f"El camino no pasa por la celda con el tesoro.")
    return path_errors

def check_solution(num_rows: int, num_cols: int, treasure_pos: Vertex, g_orig: UndirectedGraph[Vertex],
                   path: Path, added_edge: Edge, opt_path_len: int) -> list[str]:
    g = UndirectedGraph(E=g_orig.E)
    all_errors = []

    # Error en added_edge ------
    added_edge_errors = check_added_edge(g, added_edge)
    all_errors.extend(added_edge_errors)

    # Error en path ------
    g.add_edge(added_edge)
    path_errors = check_path(num_rows, num_cols, treasure_pos, g, path)
    all_errors.extend(path_errors)

    # La lontitud del camino no es mínima ------
    if len(all_errors) == 0:
        path_length = len(path) - 1
        if path_length > opt_path_len:
            all_errors.append(f"El camino óptimo tiene {opt_path_len} vértices y el encontrado tiene {len(path)}.")
        elif path_length < opt_path_len:
            all_errors.append(f"Este mensaje no debería aparecer. Puede ser un bug del validador, habla con el profesor")

    return all_errors


if __name__ == '__main__':
    salida_en_read_data = salida_en_process = False
    if len(sys.argv) == 2:
        instance_dir = sys.argv[1]
    else:
        print("Use:")
        print("  python3.12 e1_test.py <instance_directory>")
        exit(1)

    print("VALIDADOR - ENTREGABLE 1")
    print("------------------------")

    for instance_full_fn in sorted(glob(f"{instance_dir}/*.i")):
        instance_fn = os.path.basename(instance_full_fn)
        print(f"{instance_fn}: <Ctrl-C para terminarlo...>", end="")
        sys.stdout.flush()
        try:
            try:
                with open(instance_full_fn) as f:
                    output = StringIO()
                    sys.stdout = output
                    data: Data = read_data(f)
                    salida_en_read_data = len(output.getvalue()) > 0
                    num_rows, num_cols, treasure_pos, g = data
                    g_orig = UndirectedGraph(E=g.E)
            except KeyboardInterrupt:
                sys.stdout = sys.__stdout__
                print(f"\r{instance_fn}: <Terminado con Ctrl-C>{' '*40}")
                continue
            except Exception as e:
                sys.stdout = sys.__stdout__
                print(f"\r{instance_fn}: EXCEPCIÓN - read_data(): {e}{' '*40}")
                continue
            finally:
                sys.stdout = sys.__stdout__

            try:
                opt_path_len = int(instance_fn.split('.')[-2].split('-')[-1])
            except Exception as e:
                print(f"\r{instance_fn}: EXCEPCIÓN - Comprobando el nombre de la instancia: {e}{' '*40}")
                continue

            try:
                output = StringIO()
                sys.stdout = output
                t0 = process_time()
                result: Result = process(data)
                path, added_edge = result
                t = process_time() - t0
                salida_en_process = len(output.getvalue()) > 0
            except KeyboardInterrupt:
                sys.stdout = sys.__stdout__
                print(f"\r{instance_fn}: <Terminado con Ctrl-C>{' '*40}")
                continue
            except Exception as e:
                sys.stdout = sys.__stdout__
                print(f"\r{instance_fn}: EXCEPCIÓN - process(): {e}{' '*40}")
                continue
            finally:
                sys.stdout = sys.__stdout__

            try:
                errors = check_solution(num_rows, num_cols, treasure_pos, g_orig, path,
                                        added_edge, opt_path_len)
            except KeyboardInterrupt:
                print(f"\r{instance_fn}: <Terminado con Ctrl-C>{' '*40}")
                continue
            except Exception as e:
                print(f"\r{instance_fn}: EXCEPCIÓN - Comprobando la solución: {e}{' '*40}")
                continue

            if len(errors) == 0:
                extra=[]
                if salida_en_read_data:
                    extra.append('read_data')
                if salida_en_process:
                    extra.append('proces')
                msg=f' - Escritura en stdout: {', '.join(extra)}' if len(extra) > 0 else ''
                print(f"\r{instance_fn}: SOLUCIÓN_VÁLIDA - {t:.3f} seg{msg}")
            else:
                print(f"\r{instance_fn}: SOLUCIÓN_ERRÓNEA - Motivos:{' ' * 40}")
                for error in errors:
                    print(f"  - {error}")

        except KeyboardInterrupt:
            print(f"\r{instance_fn}: <Terminado con Ctrl-C>                       ")

    if salida_en_read_data or salida_en_process:
        print()
        print("Penalización de un punto:")
        print(" - En al menos una instancia, 'read_data' y/o 'process' escriben en stdout.")
        print("   [No deberíais usar print en estas dos funciones]")

    print()
    print("Información importante sobre los tiempos de ejecución:")
    print(" - Los tiempos que muestra el validador no se utilizarán para la corrección.")
    print(" - Para la corrección se utilizarán los que se obtengan al ejecutar tu programa en dama.uji.es.")
    print(" - En el enunciado se te indica cómo proceder para ejecutar tu programa en dama.")
    print(" - Para no tener que estar continuamente ejecutando en dama, puedes utilizar una regla de tres para")
    print("   estimar el tiempo que deberías obtener en tu equipo para pasar las pruebas en dama.")