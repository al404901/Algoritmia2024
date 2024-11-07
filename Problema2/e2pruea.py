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


def process3(data:Data) -> Result:
    class MaxValleyPoblem(IDivideAndConquerProblem): #ni idea de como hacerlo asi
        def __init__(self, i, j):
            self.i=i
            self.j=j
        def is_simple(self) -> bool:
            print("hola")
            return self.j - self.i <= 1

        def trivial_solution(self) -> Result:
            print("hola")
            return None

        def divide(self) -> Iterator[Self]:
            c = (self.i + self.j) // 2
            yield MaxValleyPoblem(self.i, c)
            yield MaxValleyPoblem(c, self.j)

        def combine(self, solutions: Iterator[Result]) -> Result:
            c = (self.i + self.j) // 2
            for pos in (c, self.j):
                print(pos)
                # if data[currentBuilding] > data[pos]:
                #     valleyCalc=data[currentBuilding]-data[pos]
                #     if(valleyCalc>hValley):
                #         hValley=valleyCalc
                #         valleyPos=pos
                # else:
                #     currentBuilding = pos
                #     hValley = 0
                #     if valleyPos is not None:
                #         valleys.add(valleyPos)
                #     valleyPos = pos
            # currentBuilding=self.i
            # valleyPos = None
            for pos in (self.i, c):
                print(pos)
                # if data[currentBuilding] > data[pos]:
                #     valleyCalc = data[currentBuilding] - data[pos]
                #     if (valleyCalc > hValley):
                #         hValley = valleyCalc
                #         valleyPos = pos
                # else:
                #     currentBuilding = pos
                #     hValley = 0
                #     if valleyPos is not None:
                #         valleys.add(valleyPos)
                #     valleyPos = pos
            # for valley in valleys:
            #     print("Valle encontrado en {}".format(valley))
    return div_solve(MaxValleyPoblem(0, len(data)))



def show_result(result: Result):
    print(result) if not None else "NO SOLUTION"


if __name__ == "__main__":
    #data = read_data(sys.stdin)
    data = [10, 20, 15, 25, 5, 30, 5, 45, 3, 50]
    result = process3(data)
    show_result(result)
