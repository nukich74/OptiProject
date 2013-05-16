## {{{ http://code.activestate.com/recipes/576575/ (r1)
''' This program uses the stepping stone algorithum to solve
the transhipment problem. That is how to transport various quuantities
of material to various destinations minimising overall cost, given
the various costs of sending a unit from each source to each destination.
The sum of supply and demand must equal.'''


def PrintOut():
    GetDual()
    nCost = 0
    print("DEMAND" + " " * (m * 10) + "SUPPLY")
    for y in demandArray:
        print("%10i" % y)
    for x in range(n):
        for y in range(m):
            nCost += aCost[x][y] * routeArray[x][y]
            if routeArray[x][y] == 0:
                print("[<%2i>%4i]" % (aCost[x][y], dualArray[x][y]))
            else:
                print("[<%2i>(%2i)]" % (aCost[x][y], routeArray[x][y] + 0.5))
        print(" : %i" % supplyArray[x])
    print("Cost: ", nCost)


def NorthWestMethod(supplySize, demandSize):
    global routeArray
    u = 0
    v = 0
    aD = [0] * demandSize
    aS = [0] * supplySize
    while u < supplySize and v < demandSize:
        if demandArray[v] - aD[v] < supplyArray[u] - aS[u]:
            z = demandArray[v] - aD[v]
            routeArray[u][v] = z
            aD[v] += z
            aS[u] += z
            v += 1
        else:
            z = supplyArray[u] - aS[u]
            routeArray[u][v] = z
            aD[v] += z
            aS[u] += z
            u += 1


def NotOptimal(n, m):
    global PivotN
    global PivotM
    nMax = -inf
    GetDual()
    for u in range(0, n):
        for v in range(0, m):
            x = dualArray[u][v]
            if x > nMax:
                nMax = x
                PivotN = u
                PivotM = v
    return nMax > 0


def GetDual():
    global dualArray
    for u in range(0, n):
        for v in range(0, m):
            dualArray[u][v] = -0.5
            # null value
            if routeArray[u][v] == 0:
                aPath = FindPath(u, v)
                z = -1
                x = 0
                for w in aPath:
                    x += z * aCost[w[0]][w[1]]
                    z *= -1
                dualArray[u][v] = x


def FindPath(u, v):
    aPath = [[u, v]]
    if not LookHorizontally(aPath, u, v, u, v):
        print("Path error, press key", u, v)
        input()
    return aPath


def LookHorizontally(aPath, u, v, u1, v1):
    for i in range(0, m):
        if i != v and routeArray[u][i] != 0:
            if i == v1:
                aPath.append([u, i])
                return True
                # complete circuit
            if LookVertically(aPath, u, i, u1, v1):
                aPath.append([u, i])
                return True
    return False
    # not found


def LookVertically(aPath, u, v, u1, v1):
    for i in range(0, n):
        if i != u and routeArray[i][v] != 0:
            if LookHorizontally(aPath, i, v, u1, v1):
                aPath.append([i, v])
                return True
    return False
    # not found


def BetterOptimal():
    global routeArray
    aPath = FindPath(PivotN, PivotM)
    nMin = inf
    for w in range(1, len(aPath), 2):
        t = routeArray[aPath[w][0]][aPath[w][1]]
        if t < nMin:
            nMin = t
    for w in range(1, len(aPath), 2):
        routeArray[aPath[w][0]][aPath[w][1]] -= nMin
        routeArray[aPath[w - 1][0]][aPath[w - 1][1]] += nMin

# example 1
aCost = [[2, 1, 3, 3, 2, 5],
         [3, 2, 2, 4, 3, 4],
         [3, 5, 4, 2, 4, 1],
         [4, 2, 2, 1, 2, 2]]

demandArray = [30, 50, 20, 40, 30, 11]
supplyArray = [50, 40, 60, 31]

""" example 2
aCost = [[ 1, 2, 1, 4, 5, 2]
        ,[ 3, 3, 2, 1, 4, 3]
        ,[ 4, 2, 5, 9, 6, 2]
        ,[ 3, 1, 7, 3, 4, 6]]
aDemand = [ 20, 40, 30, 10, 50, 25]
aSupply = [ 30, 50, 75, 20]

 example3
aCost = [[ 5, 3, 6, 2]
        ,[ 4, 7, 9, 1]
        ,[ 3, 4, 7, 5]]
aDemand = [ 16, 18, 30, 25]
aSupply = [ 19, 37, 34]
"""
n = len(supplyArray)
m = len(demandArray)
inf = 99999999999
# Eсли случается вырожденый случай будем использовать eps, а потом можно округлять.
# Есть куча способов выбрать eps, но такой тоже возможен: добавим [eps/sizeof(demandArray)]
# Orden A., Application of the Simplex Method to a Variety of Matrix Problems
# Orden A. The transshipment problem
eps = 0.001
for i in demandArray:
    i += eps / len(demandArray)
supplyArray[1] += eps
# базовые значения
routeArray = [[0] * len(demandArray) for i in range(len(supplyArray))]
dualArray = [[-1] * len(demandArray) for i in range(len(supplyArray))]
# в методе потенциалов нам нужно найти начальное решение, лучше конечно использовать
# метод наименьшей стоимости, чтобы получить более близкое к ответу решение, но поиск будет работать дольше, поэтому
# пока реализуем метод северного угла, т.е. будем идти слева направо и сверху в низ, и постепенно заполнять таблицу.
NorthWestMethod(len(supplyArray), len(demandArray))
PivotN = -1
PivotM = -1
#PrintOut()
# Цикл, который завершится, когда после выполнения условий оптимальности плана
# Все разности потенциалов для "неизбранных" клеток должны быть > 0
while NotOptimal(len(supplyArray), len(demandArray)):
    print("PIVOTING ON", PivotN, PivotM)
    BetterOptimal()
    PrintOut()
print("FINISHED")
