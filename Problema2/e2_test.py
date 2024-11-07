# Version 1.0 (2024-10-07). Primera versión

import os
import sys
import traceback
from glob import glob
from time import process_time
from io import StringIO
from typing import Optional

# ==========================================================================================
# COMPROBACIÓN DE LAS VERSIÓN DE PYTHON
if sys.version_info < (3, 12):
    print(f"ERROR: Este entregable necesita Python 3.12 o superior (tu versión es la {sys.version_info[0]}.{sys.version_info[1]}).", file=sys.stderr)
    exit(1)
# ==========================================================================================

from e2pruea import read_data, process, Data, Result


def show_exception(m: str, info):
    print(m)
    for l in traceback.format_exception(*info):
        if "e2_test" not in l:
            print(f" >> {l}", end="")
    print()


def read_instance(name: str, instance_fn: str) -> Optional[Data]:
    global salida_en_read_data
    try:
        with open(instance_full_fn) as f:
            output = StringIO()
            sys.stdout = output
            try:
                data: Data = read_data(f)
            finally:
                sys.stdout = sys.__stdout__
            salida_en_read_data = len(output.getvalue()) > 0
            return data
    except Exception as e:
        if isinstance(e, KeyboardInterrupt):
            print(f"\r{instance_fn}: <Terminado con Ctrl-C>{' '*40}")
        else:
            show_exception(f"\r{instance_fn}: EXCEPCIÓN - read_data():", sys.exc_info())
        return None


def check_solution(data: Data, result: Result, expected: Result) -> list[int]:
    if result == expected:
        return []
    if result is None:
        return ["No has encontrado solución y sí la hay"]
    errors = []
    left, right, valley, height = result
    left_ok, right_ok, valley_ok, height_ok = True, True, True, True
    if left < 0 or left >= len(data):
        errors.append("El lado izquierdo está fuera de los límites")
    if right < 0 or right >= len(data):
        errors.append("El lado derecho está fuera de los límites")
    if valley < 0 or valley >= len(data):
        errors.append("El valle está fuera de los límites")
    if len(errors) > 0:
        return errors
    if left >= right:
        return ["El lado izquierdo debe ser menor que el derecho"]
    if valley <= left or valley >= right:
        return ["El valle debe estar entre el lado izquierdo y el derecho"]
    wire = min(data[left], data[right])
    if not all(data[i] < wire for i in range(left + 1, right)):
        return ["Hay edificios que cortan el alambre"]
    if data[valley] != min(data[left+1:right]):
        return ["El valle no es el edificio más bajo entre el lado izquierdo y el derecho"]
    if height != wire - data[valley]:
        return ["La altura no está bien calculada"]
    exp_left, exp_right, exp_valley, exp_height = expected
    if height < exp_height:
        return ["La altura no es la máxima posible"]
    if height > exp_height:
        return ["La altura es mayor que la esperada, ponte en contacto con los profesores"]
    if valley < exp_valley:
        return ["El valle está a la izquierda del esperado, ponte en contacto con los profesores"]
    if valley > exp_valley:
        return [f"El valle está a la derecha del esperado: {valley} en lugar de {exp_valley}"]
    if result != expected:
        return [f"La solución no es la esperada {result} en lugar de {expected}"]


def read_result(name: str, instance_fn: str) -> Result:
    try:
        with open(name) as f:
            l = f.readline()
            if l == "NO HAY SOLUCIÓN\n":
                return None
            else:
                return tuple(int(x) for x in l.split())
    except Exception as e:
        show_exception(f"\r{instance_fn}: EXCEPCIÓN - Error leyendo el resultado esperado:", sys.exc_info())
        sys.exit(1)


def do_test(data: Data, expected: Result,
            instance_fn: str) -> Optional[tuple[float, list[str]]]:
    global salida_en_process
    try:
        output = StringIO()
        sys.stdout = output
        try:
            t0 = process_time()
            result: Result = process(data)
            t = process_time() - t0
        finally:
            sys.stdout = sys.__stdout__
        salida_en_process = len(output.getvalue()) > 0
        errors = check_solution(data, result, expected)
        return t, errors
    except Exception as e:
        if isinstance(e, KeyboardInterrupt):
            print(f"\r{instance_fn}: <Terminado con Ctrl-C>{' '*40}")
        else:
            show_exception(f"\r{instance_fn}: EXCEPCIÓN - process():", sys.exc_info())
        return None


if __name__ == '__main__':
    salida_en_read_data = salida_en_process = False
    if len(sys.argv) == 2:
        instance_dir = sys.argv[1]
    else:
        print("Usage:")
        yo = os.path.basename(sys.argv[0])
        print(f"  python3.12 {yo} <instance_directory>")
        exit(1)

    print("VALIDADOR - ENTREGABLE 2")
    print("------------------------")

    instances = glob(f"{instance_dir}/*.i")
    instances.sort()
    if len(instances) == 0:
        print(f"No hay ficheros de prueba en el directorio {instance_dir}")
        exit(1)

    for instance_full_fn in instances:
        instance_fn = os.path.basename(instance_full_fn)
        print(f"{instance_fn}: <Ctrl-C para terminarlo...>", end="")
        sys.stdout.flush()
        instance = read_instance(instance_full_fn, instance_fn)
        if instance is None:
            continue

        expected = read_result(instance_full_fn.replace(".i", ".o"), instance_fn)

        test_result = do_test(instance, expected, instance_fn)
        if test_result is None:
            continue
        t, errors = test_result

        if len(errors) == 0:
            extra = []
            if salida_en_read_data:
                extra.append('read_data')
            if salida_en_process:
                extra.append('process')
            msg = f' - Escritura en stdout: {', '.join(extra)}' if len(extra) > 0 else ''
            print(f"\r{instance_fn}: SOLUCIÓN_VÁLIDA - {t:.3f} seg{msg}")
        else:
            print(f"\r{instance_fn}: SOLUCIÓN_ERRÓNEA - Motivos:{' ' * 40}")
            for error in errors:
                print(f"  - {error}")

    if salida_en_read_data or salida_en_process:
        print()
        print("Penalización de un punto:")
        if salida_en_read_data and salida_en_process:
            print(" - En al menos una instancia, 'read_data' y 'process' escriben en stdout.")
            print("   [No deberíais usar print en ninguna de estas dos funciones]")
        elif salida_en_read_data:
            print(" - En al menos una instancia, 'read_data' escribe en stdout.")
            print("   [No deberíais usar print en esta función]")
        else:
            print(" - En al menos una instancia, 'process' escribe en stdout.")
            print("   [No deberíais usar print en esta función]")

    print()
    print("Información importante sobre los tiempos de ejecución:")
    print(" - Los tiempos que muestra el validador no se utilizarán para la corrección.")
    print(" - Para la corrección se utilizarán los que se obtengan al ejecutar tu programa en dama.uji.es.")
    print(" - En el enunciado se te indica cómo proceder para ejecutar tu programa en dama.")
    print(" - Para no tener que estar continuamente ejecutando en dama, puedes utilizar una regla de tres para")
    print("   estimar el tiempo que deberías obtener en tu equipo para pasar las pruebas en dama.")
