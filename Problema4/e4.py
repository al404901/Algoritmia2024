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
    print(
        "ERROR: Este entregable necesita Python 3.12 o superior",
        f"(tu versión es la {sys.version_info[0]}.{sys.version_info[1]}).",
        file=sys.stderr)
    exit(1)
try:
    from algoritmia import TVERSION

    if TVERSION < (3, 1, 3): raise Exception()
except:
    print(f"ERROR: Este entregable necesita la versión 3.1.3 (o superior) de la biblioteca 'algoritmia'.",
          file=sys.stderr)
    print(f"Abre un terminal de PyCharm y ejecuta la orden:\n\tpip install algoritmia --upgrade", file=sys.stderr)
    exit(1)
# ==========================================================================================

# Tipos para representar la instancia: ----------------------

type Request = tuple[int, int]  # (pago, tiempo_máximo_espera)

# Data es el tipo devuelto por la función read_data
# Es la tupla (tiempo_IA_activa, tupla_peticiones)
type Data = tuple[int, tuple[Request, ...]]

# Tipos para representar el resultado: ----------------------

type RequestID = int  # el índice de la petición en la lista Data[1]

# Result es el tipo devuelto por la función process
# Es la tupla (beneficio, lista_peticiones_atendidas)
type Result = tuple[int, list[RequestID]]

# ------------------------------------------------------------------------------------------------

def read_data(f: TextIO) -> Data:
    # TODO: IMPLEMENTAR
    raise NotImplementedError('read_data')  # Quitar

def process(data: Data) -> Result:
    # TODO: IMPLEMENTAR
    raise NotImplementedError('process')  # Quitar

# ----- NO MODIFICAR EL PROGRAMA A PARTIR DE ESTA LÍNEA -----

def show_result(result: Result):
    profit, decisions = result
    print(profit)
    print(decisions)

# ------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    data0 = read_data(sys.stdin)
    result0 = process(data0)
    show_result(result0)
