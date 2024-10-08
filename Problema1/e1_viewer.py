import sys
import tkinter
from ast import literal_eval

# ==========================================================================================
# COMPROBACIÓN DE LAS VERSIONES DE Python Y algoritmia
if sys.version_info < (3, 12):
    pv = f"{sys.version_info[0]}.{sys.version_info[1]}"
    print(f"ERROR: Este entregable necesita Python 3.12 o superior (tu versión es la {pv}).", file=sys.stderr)
    exit(1)
try:
    from algoritmia import TVERSION
    if TVERSION < (3, 1, 3): raise Exception()
except:
    print(f"ERROR: Este entregable necesita la versión 3.1.3 (o superior) de la biblioteca 'algoritmia'.", file=sys.stderr)
    print(f"Abre un terminal de PyCharm y ejecuta la orden:\n\tpip install algoritmia --upgrade", file=sys.stderr)
    exit(1)
# ==========================================================================================

from algoritmia.datastructures.graphs import UndirectedGraph
from algoritmia.viewers.labyrinth_viewer import LabyrinthViewer

from e1 import read_data
from e1_test import check_added_edge, check_path

def get_screen_size() -> tuple[int, int]:
    screen = tkinter.Tk()
    max_w, max_h = screen.maxsize()
    screen.after(1, lambda: screen.destroy())
    screen.mainloop()
    # return max_w, max_h
    return int(0.95*max_w), int(0.95*max_h)

if __name__ == '__main__':
    instance_fn = solution_fn = ''
    if len(sys.argv) == 2:
        instance_fn = sys.argv[1]
    elif len(sys.argv) == 3:
        instance_fn = sys.argv[1]
        solution_fn = sys.argv[2]
    else:
        print("Uso:")
        print(" - Ver una instancia como laberinto: python3.12 e1_viewer.py <instance_filename>")
        print(" - Ver una instancia y su solución:  python3.12 e1_viewer.py <instance_filename> <solution_filename>")
        exit(1)

    try:
        with open(instance_fn) as f:
            num_rows, num_cols, treasure_pos, g = read_data(f)
            g_orig = UndirectedGraph(E=g.E)
    except Exception as e:
        print(f"ERROR. Al leer la instancia con read_data() se lanzó una excepción: {e}", file=sys.stderr)
        exit(1)

    path_error = []
    added_edge = -1, -1
    if solution_fn != '':
        try:
            if solution_fn == '-':
                path = literal_eval(sys.stdin.readline())
                path_length = literal_eval(sys.stdin.readline())
                added_edge = literal_eval(sys.stdin.readline())
                g.add_edge(added_edge)
            else:
                with open(solution_fn) as f:
                    path = literal_eval(f.readline())
                    path_length = literal_eval(f.readline())
                    added_edge = literal_eval(f.readline())
                    g.add_edge(added_edge)
        except Exception as e:
            print(f"ERROR. Al leer la solución se lanzó una excepción: {e}", file=sys.stderr)
            exit(1)

        path_error.extend(check_added_edge(g_orig, added_edge))
        path_error.extend(check_path(num_rows, num_cols, treasure_pos, g, path))

        if len(path_error) > 0:
            print(f"ERROR - El camino no es válido. Motivos:")
            for error in path_error:
                print(f"  - {error}")

    max_width, max_height = get_screen_size()
    print(max_width, max_height)
    cell_size = min(max_width//num_cols, max_height//num_rows)
    cell_size = min(cell_size, 60)
    margin = 4
    canvas_height = num_rows * cell_size + 2 * margin
    canvas_width = num_cols * cell_size + 2 * margin
    wall_width = 2 if cell_size > 20 else 1

    lv = LabyrinthViewer(g, title="Visor entregagle 1",
                         margin=margin, wall_width=wall_width,
                         canvas_width=canvas_width,
                         canvas_height=canvas_height)

    # Marca de verde la celda con el tesoro
    lv.add_marked_cell(treasure_pos, color='lightgreen')

    # Marca la entrada y la salida
    lv.set_input_point((0, 0))
    lv.set_output_point((num_rows - 1, num_cols - 1))

    if solution_fn != '':
        # Marca de naranja las celdas que comparten la pared eliminada
        if added_edge[0] in g.V:
            lv.add_marked_cell(added_edge[0], color='orange')
        if added_edge[1] in g.V:
            lv.add_marked_cell(added_edge[1], color='orange')

        # Añade una línea roja con el camino de la entrada al tesoro
        if treasure_pos in path:
            tp = path.index(treasure_pos)
            lv.add_path(path[:tp + 1], 'red', 1)

            # Añade una línea azul con el camino del tesoro a la salida
            lv.add_path(path[tp:], 'blue', -1)
        else:
            lv.add_path(path, 'green', 1)

    # Muestra la ventana gráfica
    lv.run()
