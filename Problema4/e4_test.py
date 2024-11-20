import os
import sys
from copy import deepcopy
from glob import glob
from time import process_time
from io import StringIO

# ==========================================================================================
# COMPROBACIÓN DE LAS VERSIONES DE Python Y algoritmia
if sys.version_info < (3, 12):
    print(
        f"\nERROR: Este entregable necesita Python 3.12 o superior",
        f"(tu versión es la {sys.version_info[0]}.{sys.version_info[1]}).\n",
        file=sys.stderr)
    exit(1)
try:
    from algoritmia import TVERSION

    if TVERSION < (3, 1, 3): raise Exception()
except Exception:
    print(f"ERROR: Este entregable necesita la versión 3.1.3 o superior de la biblioteca 'algoritmia'.",
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
# Importar read_data y process de e4.py

try:
    from e4 import read_data, process
except Exception as e:
    print(f"EXCEPCIÓN - importando e4.py: [{e.__class__.__name__}: {e}]")
    exit(1)

# ------------------------------------------------------------------------------------------------
# Funciones para comprobar los tipos de los objetos devueltos por read_data y process

def is_valid_Data(data: Data) -> bool:
    if not isinstance(data, tuple) or len(data) != 2:
        return False
    mmax_wait_time, request = data
    if not isinstance(mmax_wait_time, int):
        return False
    if not isinstance(request, tuple):
        return False
    for r in request:
        if not isinstance(r, tuple) or list(map(type, r)) != [int, int]: return False
    return True

def is_valid_Result(result: Result) -> bool:
    if not isinstance(result, tuple) or len(result) != 2:
        return False
    amount, decisions = result
    if not isinstance(amount, int): return False
    for decision in decisions:
        if not isinstance(decision, int): return False
    return True

# ------------------------------------------------------------------------------------------------
# Funciones para comprobar los objetos devueltos por read_data y process

def check_read_data(instance_full_fn: str) -> tuple[Data, bool] | None:
    instance_fn = os.path.basename(instance_full_fn)
    try:
        with open(instance_full_fn) as f:
            output = StringIO()
            sys.stdout = output
            data: Data = read_data(f)
            if not is_valid_Data(data):
                raise RuntimeError("El objeto devuelto no es de tipo 'Data'")
            stdout_is_clean = len(output.getvalue()) == 0
    except KeyboardInterrupt:
        sys.stdout = sys.__stdout__
        print(f"\r{instance_fn}: <Terminado con Ctrl-C>{' ' * 40}")
        return
    except Exception as ex:
        sys.stdout = sys.__stdout__
        print(f"\r{instance_fn}: EXCEPCIÓN - read_data(): [{ex.__class__.__name__}: {ex}]{' ' * 40}")
        return
    finally:
        sys.stdout = sys.__stdout__
    return data, stdout_is_clean

def check_process(data: Data) -> tuple[Result, bool, float] | None:
    instance_fn = os.path.basename(instance_full_fn0)
    try:
        output = StringIO()
        sys.stdout = output
        t0 = process_time()
        result: Result = process(data)
        tt = process_time() - t0
        if not is_valid_Result(result):
            raise RuntimeError("El objeto devuelto no es de tipo 'Result'")
        stdout_is_clean = len(output.getvalue()) == 0
    except KeyboardInterrupt:
        sys.stdout = sys.__stdout__
        print(f"\r{instance_fn}: <Terminado con Ctrl-C>{' ' * 40}")
        return
    except Exception as ex:
        sys.stdout = sys.__stdout__
        print(f"\r{instance_fn}: EXCEPCIÓN - process(): [{ex.__class__.__name__}: {ex}]{' ' * 40}")
        return
    finally:
        sys.stdout = sys.__stdout__
    return result, stdout_is_clean, tt


def check_solution(instance_fn: str, use_stdout: list[str], p_time: float,
                   data: Data, result: Result) -> float:
    class BadSolution(Exception):
        pass

    best_amount = int(instance_fn.split('-')[-1][:-2])
    try:
        n, request = data
        user_amount, decisions = result
        if len(decisions) != n:
            raise BadSolution(f"La lista de peticiones atendidas debe tener {n} elementos (tiene {len(decisions)})")
        seen = set()
        for d in decisions:
            if d == -1:
                continue
            if d in seen:
                raise BadSolution(f"La lista de peticiones atendidas tiene repeticiones")
            seen.add(d)

        amount2 = 0
        peticiones_fuera_de_plazo = False
        for i, d in enumerate(decisions):
            if d == -1: continue
            if i < request[d][1]:
                amount2 += request[d][0]
            else:
                peticiones_fuera_de_plazo = True

        if amount2 != user_amount:
            raise BadSolution(f"El beneficio devuelto ({user_amount}) no coincide con el de tu solución ({amount2})")

        pp = user_amount/best_amount
        minimo = 0.5
        score = (pp - minimo) / (1 - minimo) if pp > minimo else 0

        msg = ""
        if len(use_stdout) > 0:
            msg += f' - Escritura en stdout: {', '.join(use_stdout)}'

        print(f"\r{instance_fn}: SOLUCIÓN_VÁLIDA - {p_time:.3f} seg [Beneficio: {user_amount} - Puntuación: {score:.2f}]{msg}{' ' * 40}")
        return score

    except KeyboardInterrupt:
        print(f"\r{instance_fn}: <Terminado con Ctrl-C>{' ' * 40}")
    except BadSolution as d:
        print(f"\r{instance_fn}: SOLUCIÓN_ERRÓNEA - Motivo: {d}{' ' * 40}")
    except Exception as d:
        print(f"\r{instance_fn}: EXCEPCIÓN - Comprobando la solución: {d}{' ' * 40}")
    return 0

# ------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    if len(sys.argv) == 2:
        instance_dir = sys.argv[1]
    else:
        print("Use:")
        print("  python3.12 -O e4_test.py <instance_directory>")
        exit(1)

    print("VALIDADOR - ENTREGABLE 4")
    print("------------------------")
    use_stdout0 = False

    total_score = 0
    for instance_full_fn0 in sorted(glob(f"{instance_dir}/*.i")):
        instance_fn0 = os.path.basename(instance_full_fn0)
        print(f"{instance_fn0}: <Ctrl-C para terminarlo...>", end="")
        sys.stdout.flush()

        try:
            use_stdout0 = []

            res = check_read_data(instance_full_fn0)
            if res is None:
                continue
            data0, stdout_is_clean0 = res
            if not stdout_is_clean0:
                use_stdout0.append('read_data')

            data0_copy = deepcopy(data0)
            res = check_process(data0_copy)
            if res is None:
                continue
            result0, stdout_is_clean0, t = res
            if not stdout_is_clean0:
                use_stdout0.append('process')

            total_score += check_solution(instance_fn0, use_stdout0, t, data0, result0)

        except KeyboardInterrupt:
            print(f"\r{instance_fn0}: <Terminado con Ctrl-C>{' ' * 40}")

    print(f"Puntuacion final (sobre 10): {total_score:.2f}\n")

    if len(use_stdout0) > 0:
        print()
        print("Penalización de un punto:")
        print(" - En al menos una instancia, 'read_data' y/o 'process' escriben en stdout.")
        print("   [Recuerda quitar esos 'print' antes de entregar]")

    print()
    print("Información importante sobre los tiempos de ejecución:")
    print(" - Los tiempos que muestra el validador no se utilizarán para la corrección.")
    print(" - Para la corrección se utilizarán los que se obtengan al ejecutar tu programa en 'rei.dlsi.uji.es'.")
    print(" - En el enunciado se te indica cómo proceder para ejecutar tu programa en 'rei'.")
    print(" - Para no tener que estar continuamente ejecutando en 'rei', puedes utilizar una regla de tres para")
    print("   estimar el tiempo que deberías obtener en tu equipo para pasar las pruebas en 'rei'.")
