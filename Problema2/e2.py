import sys
from typing import TextIO, Iterable, Iterator, Self

from algoritmia.schemes.dac_scheme import IDivideAndConquerProblem, Solution, div_solve

# ------ Tipos ------

# Data es el tipo devuelto por read_data()
# Es una lista de alturas
type Data = list[int]

# Result es el tipo devuelto por process()
# Es none o la tupla: (left, right, valley, height)
type Result = None | tuple[int, int, int, int]

# ----- Funciones -----

def read_data(f: TextIO) -> Data:
    buildings=[]
    for line in f.readlines():
        buildings.append(int(line))
    return buildings

# def process(data: Data) -> Result:
#     class MaxValleyProblem(IDivideAndConquerProblem):
#         def __init__(self, i: int, j: int):
#             self.i = i
#             self.j = j
#
#         def is_simple(self) -> bool:
#             return self.j - self.i <= 1
#
#         def trivial_solution(self) -> Result:
#             return None
#
#         def divide(self) -> Iterator['MaxValleyProblem']:
#             c = (self.i + self.j) // 2
#             yield MaxValleyProblem(self.i, c)
#             yield MaxValleyProblem(c, self.j)
#
#         def combine(self, solutions: Iterator[Result]) -> Result:
#             max_height = -1
#             best_solution = None
#
#             # Loop to find valid combinations
#             for left in range(self.i, self.j):
#                 for right in range(left + 1, self.j):
#                     height = min(data[left], data[right])
#                     valley_found = False
#                     valley_index = -1
#                     for k in range(left + 1, right):
#                         if data[k] >= height:
#                             break
#                         valley_found = True
#                         valley_index = k
#
#                     if valley_found:
#                         valley_height = height - data[valley_index]
#                         if valley_height > max_height or (valley_height == max_height and (best_solution is None or valley_index < best_solution[2])):
#                             max_height = valley_height
#                             best_solution = (left, right, valley_index, valley_height)
#
#             return best_solution if best_solution else None
#     return div_solve(MaxValleyProblem(0, len(data)))



def process(data:Data) -> Result:
    class MaxValleyPoblem(IDivideAndConquerProblem): #ni idea de como hacerlo asi
        def __init__(self, i, j):
            self.i=i
            self.j=j
        def is_simple(self) -> bool:
            return self.j - self.i <= 1
            pass

        def trivial_solution(self) -> Result:
            return None

        def divide(self) -> Iterator[Self]:
            c = (self.i + self.j) // 2
            yield MaxValleyPoblem(self.i, c)
            yield MaxValleyPoblem(c, self.j)

        def combine(self, solutions: Iterator[Result]) -> Result:
            c = (self.i + self.j) // 2
            hValley = 0
            posBuilding = c
            valleys: set[int]
            for pos in range(self.j - 1, c - 1, - 1):
                print("Leyendo posición: {}, altura: {}".format(pos, data[pos]))
                if data[pos] >= data[posBuilding]:
                    posbuilding = pos
                    print("entro aqui")
                else:
                    valleyCalc = data[posBuilding]-data[pos]
                    print("valleyCalc: {}".format(valleyCalc))
                    if valleyCalc > hValley:
                        hValley=valleyCalc
            print(hValley)
            for pos in range(self.i, c):
                print("Leyendo posición: {}, altura: {}".format(pos, data[pos]))
                if data[pos] >= data[posBuilding]:
                    posbuilding = pos
                    print("entro aqui")
                else:
                    valleyCalc = data[posBuilding]-data[pos]
                    print("valleyCalc: {}".format(valleyCalc))
                    if valleyCalc > hValley:
                        hValley=valleyCalc

            print(hValley)
            #max(bsol)
            #return max(bsol, (hValley, b, e))

    return div_solve(MaxValleyPoblem(0, len(data)))
    # if problem.is_simple():
    #     return problem.trivial_solution()
    # else:
    #     subproblems = problem.divide()
    #     solutions = (div_solve(p) for p in subproblems)
    #     return problem.combine(solutions)

#valle = 0
#ed1 = 0
#ed2 = 0
#solucionEnDerecha = false
#for elem in range(c,j)
#calculo = data[edificio] - data[elem]:
#if calculo > valle
#valle = calculo
#ed1 = elem
#(fuera del for)posicion = ed1 + 1
#   while(posicion < len(data))
#       if data[posicion] >= data[ed1]:
 #           ed2 = posicion
 #           break
 #       posicion+=1


#POSIBLE SOLUCION: MIRAR DE LOS BORDES AL MEDIO

def process1(data: Data) -> Result:
    def funambulist(i, j):
        if j-i <= 1: #is_simple
            if i == j: #trivial
                return None
            return None
        c = (i+j)//2
        right = funambulist(c, j)
        left = funambulist(i, c)
        alturaValley = 0
        alturaValleyProv=0
        indexValley1, indexValley2 = c, c
        #programar desde aqui
        alturaValley1 = 0
        posicionEdificio1 = 0
        posicionEdificio2 = 0
        edificioMedio = c
        centroAux = c
        for pos in range(c + 1, j):
            print("Leyendo posición: {}, altura: {}".format(pos, data[pos]))
            if data[pos] >= data[centroAux]:
                centroAux = pos
            else:
                calculoValle = data[centroAux] - data[pos]
                if calculoValle > alturaValley1:
                    alturaValley1=calculoValle
                    indexValley1=pos
        alturaValleyProv=0
        #print("Mejor valle encontrado {} calculando desde edificio {} menos edificio {}".format(alturaValley1, centroAux, indexValley1))
        alturaValley2 = 0
        posicionEdificio3 = 0
        posicionEdificio4 = 0
        edificioMedio = c
        centroAux2 = c
        for pos in range(c - 1, i - 1, -1):
            print("Leyendo posición: {}, altura: {}".format(pos, data[pos]))
            if data[pos] >= data[centroAux2]:
                centroAux2 = pos
            else:
                calculoValle = data[centroAux2] - data[pos]
                if calculoValle > alturaValley2:
                    alturaValley2 = calculoValle
                    indexValley2=pos
        #print("Mejor valle encontrado {} calculando desde edificio {} menos edificio {}".format(alturaValley2, centroAux2, indexValley2))
    return funambulist(0, len(data))
        # for pos in range(c - 1, i - 1, -1):
        #     if data[pos] > data[posBuilding]:
        #         posBuilding = pos
        #     else:
        #         if posBuilding!=j-1:
        #             valleyCalc = data[posBuilding] - data[pos]
        #             if valleyCalc > hValley:
        #                 posValley = pos
        #                 hValley = valleyCalc
        #                 buildingWithValley = posBuilding

        #return max(left, right (hValley, buildingWithValley, posValley))
        #print("Inicio en centro: {} . El valle más bajo es {}, posición {} || Edificio izquierdo con posición: {}".format(c, hValley, posValley, buildingWithValley))
    #return funambulist(0, len(data))


def show_result(result: Result):
    print(result) if not None else "NO SOLUTION"


if __name__ == "__main__":
    data = read_data(sys.stdin)
    #data = [10, 20, 15, 25, 5, 30, 5, 45, 3, 50]
    result = process(data)
    show_result(result)
