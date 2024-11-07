import sys
from typing import TextIO, Iterable, Iterator, Self

from algoritmia.schemes.dac_scheme import div_solve, IDivideAndConquerProblem

# ------ Tipos ------

# Data es el tipo devuelto por read_data()
# Es una lista de alturas
type Data = list[int]

# Result es el tipo devuelto por process()
# Es none o la tupla: (left, right, valley, height)
type Result = None | tuple[int, int, int, int]

# ----- Funciones -----

def read_data(f: TextIO) -> Data:
    buildings = []
    for line in f.readlines():
        buildings.append(int(line))
    return buildings



def process(data: Data) -> Result:
    class MaxValleyPoblem(IDivideAndConquerProblem):  # ni idea de como hacerlo asi
        def __init__(self, i, j):
            self.i = i
            self.j = j

        def is_simple(self) -> bool:
            return self.j - self.i <= 1

        def trivial_solution(self) -> Result:
            return None

        def divide(self) -> Iterator[Self]:
            c = (self.i + self.j) // 2
            yield MaxValleyPoblem(self.i, c)
            yield MaxValleyPoblem(c, self.j)

        def combine(self, solutions: Iterator[Result]) -> Result:
            c = (self.i + self.j) // 2
            sumH=0
            sumHMax=0
            hValley=0
            valleyPosFinal=None
            leftBuilding = 0
            rightBuilding = 0
            maxBuildingPos=0
            currentL=self.i
            for pos in range(self.i, c):
                if pos != self.i:
                    if data[pos] < data[prev]:
                        valleyCalc=data[prev]-data[pos]
                        if valleyCalc > hValley:
                            sumH+=valleyCalc
                            hValley=valleyCalc
                            valleyPos=pos
                    elif data[pos] >= data[prev]:
                        print(sumH, sumHMax, data[pos], data[prev], data[currentL])
                        if sumH > sumHMax:
                            sumHMax=sumH
                            valleyPosFinal=valleyPos
                            currentL = pos
                        sumH=0
                        hValley=0
                prev=pos
            sumH = 0
            hValley = 0
            for pos in range(c, self.j):
                if pos != c:
                    if data[pos] < data[prev]:
                        valleyCalc=data[prev]-data[pos]
                        if valleyCalc > hValley:
                            sumH+=valleyCalc
                            hValley=valleyCalc
                            valleyPos=pos
                    elif data[pos] >= data[prev]:
                        print(sumH, sumHMax, data[pos], data[prev], data[currentL])
                        if sumH > sumHMax:
                            sumHMax=sumH
                            valleyPosFinal=valleyPos
                        sumH=0
                        hValley=0

                prev=pos
                #print("Valle en posición {}, altura cable {}".format(valleyPosFinal, sumHMax))
            for pos in range(valleyPosFinal-1, self.i-1, -1):
                if data[pos]-data[valleyPosFinal]==sumHMax:
                    leftBuilding=pos

                    break

            print(leftBuilding, rightBuilding, valleyPosFinal, sumHMax)
    return div_solve(MaxValleyPoblem(0, len(data)))


def show_result(result: Result):
    print(result) if not None else "NO SOLUTION"


if __name__ == "__main__":
    data = read_data(sys.stdin)
    result = process(data)
    show_result(result)
