import os
import sys
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
type Weight = int
type Value = int
type Item = tuple[Weight, Value]
type Data = tuple[Value, tuple[Weight, Weight], tuple[Item, ...]]

# Tipos para representar el resultado: ----------------------
type Decision = int                                 # 0, 1 o -1
type Solution = tuple[Value, tuple[Decision, ...]]
type Result = Solution | None

# ------------------------------------------------------------------------------------------------
# Importar read_data y process de e3.py

try:
    from e3 import read_data, process
except Exception as e:
    print(f"EXCEPCIÓN - importando e3.py: [{e.__class__.__name__}: {e}]")
    exit(1)

# ------------------------------------------------------------------------------------------------
# Funciones para comprobar los tipos de los objetos devueltos por read_data y process

def is_valid_Data(data: Data) -> bool:
    if not isinstance(data, tuple) or len(data) != 3:
        return False
    min_value, caps, items = data
    if not isinstance(min_value, int): return False
    if not isinstance(caps, tuple) or list(map(type, caps)) != [int, int]: return False
    if not isinstance(items, tuple): return False
    for item in items:
        if not isinstance(item, tuple) or list(map(type, item)) != [int, int]: return False
    return True

def is_valid_Solution(solution: Solution) -> bool:
    if not isinstance(solution, tuple) or len(solution) != 2:
        return False
    value, decisions = solution
    if not isinstance(value, int): return False
    if not isinstance(decisions, tuple): return False
    for decision in decisions:
        if not isinstance(decision, int): return False
    return True

def is_valid_Result(result: Result) -> bool:
    return result is None or is_valid_Solution(result)

# ------------------------------------------------------------------------------------------------
# Funciones para comprobar los objetos devueltos por read_data y process

def check_read_data(instance_full_fn: str) -> tuple[Data, bool] | None:
    instance_fn = os.path.basename(instance_full_fn)
    try:
        with open(instance_full_fn) as f:
            output = StringIO()
            sys.stdout = output
            data0: Data = read_data(f)
            if not is_valid_Data(data0):
                raise RuntimeError("El objeto devuelto no es de tipo 'Data'")
            stdout_is_clean = len(output.getvalue()) == 0
    except KeyboardInterrupt:
        sys.stdout = sys.__stdout__
        print(f"\r{instance_fn}: <Terminado con Ctrl-C>{' ' * 40}")
        return
    except Exception as e:
        sys.stdout = sys.__stdout__
        print(f"\r{instance_fn}: EXCEPCIÓN - read_data(): [{e.__class__.__name__}: {e}]{' ' * 40}")
        return
    finally:
        sys.stdout = sys.__stdout__
    return data0, stdout_is_clean

def check_process(data0: Data) -> tuple[Result, bool, float] | None:
    instance_fn = os.path.basename(instance_full_fn)
    try:
        output = StringIO()
        sys.stdout = output
        t0 = process_time()
        result0: Result = process(data0)
        t = process_time() - t0
        if not is_valid_Result(result0):
            raise RuntimeError("El objeto devuelto no es de tipo 'Result'")
        stdout_is_clean = len(output.getvalue()) == 0
    except KeyboardInterrupt:
        sys.stdout = sys.__stdout__
        print(f"\r{instance_fn}: <Terminado con Ctrl-C>{' ' * 40}")
        return
    except Exception as e:
        sys.stdout = sys.__stdout__
        print(f"\r{instance_fn}: EXCEPCIÓN - process(): [{e.__class__.__name__}: {e}]{' ' * 40}")
        return
    finally:
        sys.stdout = sys.__stdout__
    return result0, stdout_is_clean, t

def check_solution(instance_fn: str, use_stdout: list[str], t: float,
                   data: Data, result: Result, has_sol: bool):
    class BadSolution(Exception):
        pass

    try:
        min_value, capacities, items = data
        if result is None:
            if has_sol:
                raise BadSolution("Hay al menos una solución, pero tu programa no ha encontrado ninguna")
        else:
            if not has_sol:
                raise BadSolution("No hay solución, pero tu programa ha devuelto una incorrecta")

            solution_value, solution = result

            if solution_value < min_value:
                raise BadSolution("Tu solución no alcanza el valor mínimo solicitado para el conjunto de las mochilas")

            ks = list(capacities)
            calc_value = 0
            for i, ki in enumerate(solution):
                if ki == -1: continue
                if ks[ki] < items[i][0]:
                    raise BadSolution("Tu solución se pasa de peso con la mochila con índice {ki} (contando desde 0)")
                ks[ki] -= items[i][0]
                calc_value += items[i][1]

            if calc_value != solution_value:
                raise BadSolution("El valor del contenido de tus dos mochilas no es el que indicas")

        if len(use_stdout) > 0:
            msg = f' - Escritura en stdout: {', '.join(use_stdout)}'
            print(f"\r{instance_fn}: SOLUCIÓN_VÁLIDA - {t:.3f} seg{msg}{' ' * 40}")

        print(f"\r{instance_fn}: SOLUCIÓN_VÁLIDA - {t:.3f} seg{' ' * 40}")

    except KeyboardInterrupt:
        print(f"\r{instance_fn}: <Terminado con Ctrl-C>{' ' * 40}")
    except BadSolution as e:
        print(f"\r{instance_fn}: SOLUCIÓN_ERRÓNEA - Motivo: {e}{' ' * 40}")
    except Exception as e:
        print(f"\r{instance_fn}: EXCEPCIÓN - Comprobando la solución: {e}{' ' * 40}")

# ------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    if len(sys.argv) == 2:
        instance_dir = sys.argv[1]
    else:
        print("Use:")
        print("  python3.12 e3_test.py <instance_directory>")
        exit(1)

    print("VALIDADOR - ENTREGABLE 3")
    print("------------------------")
    use_stdout = False

    for instance_full_fn in sorted(glob(f"{instance_dir}/*.i")):
        solution_full_fn = instance_full_fn[:-1] + 'o'
        instance_fn = os.path.basename(instance_full_fn)
        print(f"{instance_fn}: <Ctrl-C para terminarlo...>", end="")
        sys.stdout.flush()

        with open(solution_full_fn) as f:
            has_sol0 = f.readline().strip() != 'IMPOSSIBLE'

        try:
            use_stdout = []

            res = check_read_data(instance_full_fn)
            if res is None:
                continue
            data0, stdout_is_clean = res
            if not stdout_is_clean:
                use_stdout.append('read_data')

            res = check_process(data0)
            if res is None:
                continue
            result0, stdout_is_clean, t = res
            if not stdout_is_clean:
                use_stdout.append('process')

            check_solution(instance_fn, use_stdout, t, data0, result0, has_sol0)

        except KeyboardInterrupt:
            print(f"\r{instance_fn}: <Terminado con Ctrl-C>{' '*40}")

    if len(use_stdout) > 0:
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
