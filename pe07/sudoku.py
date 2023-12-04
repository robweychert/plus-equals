import itertools

rowNum = 5
sudokuRows = []
for i in range(rowNum):
    sudokuRows.append(i+1)
sudokuRows = list(itertools.permutations(sudokuRows))

# print(str(len(sudokuRows)) + ' sudoku rows')

def compareRows(rowSet,newRow):
    compatible = True
    for row in rowSet:
        if compatible:
            for i in range(len(row)):
                if row[i] == newRow[i]:
                    compatible = False
                    break
    return compatible

index = 34
comparisons = 0
row2 = []
row3 = []
row4 = []
row5 = []

# print('--------------------')
# print('index: ' + str(index))
# print('--------------------')
for sudokuRowSet in sudokuRows:
    comparisons += 1
    if compareRows([sudokuRowSet], sudokuRows[index]) == True:
        pair = [sudokuRows[index], sudokuRowSet]
        row2.append(pair)
# print(str(len(row2)) + ' compatible row pairs')

for sudokuRowSet in row2:
    for sudokuRow in sudokuRows:
        comparisons += 1
        if compareRows(sudokuRowSet, sudokuRow) == True:
            trio = sudokuRowSet.copy()
            trio.append(sudokuRow)
            row3.append(trio)
# print(str(len(row3)) + ' compatible row trios')

for sudokuRowSet in row3:
    for sudokuRow in sudokuRows:
        comparisons += 1
        if compareRows(sudokuRowSet, sudokuRow) == True:
            quartet = sudokuRowSet.copy()
            quartet.append(sudokuRow)
            row4.append(quartet)
# print(str(len(row4)) + ' compatible row quartets')
# print(row4)

for sudokuRowSet in row4:
    for sudokuRow in sudokuRows:
        comparisons += 1
        if compareRows(sudokuRowSet, sudokuRow) == True:
            quintet = sudokuRowSet.copy()
            quintet.append(sudokuRow)
            row5.append(quintet)
# print(str(len(row5)) + ' compatible row quintets')
# print(str(comparisons) + ' comparisons')

allSudokus = []
for i in range(len(row5)):
    perms = list(itertools.permutations(row5[i]))
    for perm in perms:
        allSudokus.append(perm)
allSudokus.sort()
print(str(len(allSudokus)) + ' possible 5×5 sudokus')

def compareSudokus(sudoku1,sudoku2):
    compatible = True
    for i in range(len(sudoku1)):
        if compatible:
            for j in range(len(sudoku1[i])):
                if sudoku1[i][j] == sudoku2[i][j]:
                    compatible = False
                    break
    return compatible

bilateralSudokus = []

# for sudoku1 in allSudokus:
#     for sudoku2 in allSudokus:
#         if compareSudokus(sudoku1,sudoku2) == True:
#             newBilateralSudoku = [sudoku1,sudoku2]
#             if newBilateralSudoku not in bilateralSudokus:
#                 bilateralSudokus.append(newBilateralSudoku)

for sudoku1 in allSudokus:
    sudoku2 = allSudokus[index]
    if compareSudokus(sudoku1,sudoku2) == True:
        newBilateralSudoku = [sudoku1,sudoku2]
        if newBilateralSudoku not in bilateralSudokus:
            bilateralSudokus.append(newBilateralSudoku)
print(str(len(bilateralSudokus)) + ' bilateral sudokus for index ' + str(index))

final = []
for bs in bilateralSudokus:
    pairs = []
    legal = True
    for i in range(5):
        if legal:
            for j in range(5):
                pair = [bs[0][i][j], bs[1][i][j]]
                if pair not in pairs:
                    pairs.append(pair)
                else:
                    legal = False
                    break
    if legal:
        final.append(bs)
print(str(len(final)) + ' legal')