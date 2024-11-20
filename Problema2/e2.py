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
            minHeightLeft=None
            minHeightRight=None
            for pos in range(self.i, c):
                if minHeightLeft is None or data[pos] < minHeightLeft[1] :
                    minHeightLeft = pos, data[pos]
            maxLeft = minHeightLeft[0]
            leftBuilding = minHeightLeft[0]
            for pos in range(minHeightLeft[0], c+1):
                if data[pos]>data[maxLeft]:
                    maxLeft=pos
            for pos in range(minHeightLeft[0]-1, self.i-1, -1):
                if data[pos]>data[maxLeft]:
                    break
                if data[leftBuilding] < data[pos]:
                    leftBuilding = pos
            for pos in range(c, self.j):
                if minHeightRight is None or data[pos] < minHeightRight[1] :
                    minHeightRight = pos, data[pos]
            maxRight = minHeightRight[0]
            leftBuilding2=minHeightRight[0]
            for pos in range(minHeightRight[0], self.j):
                if data[pos]>data[maxRight]:
                    maxRight=pos
            for pos in range(minHeightRight[0]-1, c-1, -1):
                if data[pos]>data[maxRight]:
                    break
                if data[leftBuilding2] < data[pos]:
                    leftBuilding2=pos
            cableHeight=data[leftBuilding]-minHeightLeft[1]
            cableHeight2=data[leftBuilding2]-minHeightRight[1]
            solution=None
            if cableHeight<cableHeight2:
                solution=leftBuilding2, maxRight, minHeightRight[0], cableHeight2
            else:
                solution=leftBuilding, maxLeft, minHeightLeft[0], cableHeight
            return solution
    return div_solve(MaxValleyPoblem(0, len(data)))


def show_result(result: Result):
    print(result) if not None else "NO SOLUTION"


if __name__ == "__main__":
    data = read_data(sys.stdin)
    result = process(data)
    show_result(result)
