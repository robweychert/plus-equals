# Read Plus Equals #7 (https://plusequals.art/07) for the
# backstory on this script. Run the script in DrawBot
# (https://drawbot.com).

#------------------------------
# Settings
#------------------------------

import pe07_symmetry_yes_final
selections = pe07_symmetry_yes_final.selections

canvasW = 300
grid = 4
subgrid = 8
deviationMax = 2
weight = (3/1000) * canvasW
density = 12
displayGrid = False
fileNamePrefix = 'PE07-S'
fileType = 'svg' # 'pdf' or 'svg'
mutationID = 0

#------------------------------

import math
import random
import itertools

canvasH = canvasW
marginW = 4
subgridUnit = canvasW / ((grid * subgrid) + (deviationMax * 2) + (marginW * 2))
gridUnit = subgridUnit * subgrid
margin = (subgridUnit * marginW) + (subgridUnit * deviationMax)

# Make a list of every amount of subgrid units a point can
# deviate from a main grid coordinate
deviations = [0]
for i in range(deviationMax):
    deviations.append((i + 1))
    deviations.append((i + 1) * -1)
deviations.sort()

# Make a list of every possible x,y pair of subgrid deviations
deviationPairs = []
for i in range(len(deviations)):
    combo = [deviations[i]]
    for j in range(len(deviations)):
        combo.append(deviations[j])
        if combo not in deviationPairs:
            deviationPairs.append(combo)
        combo = [deviations[i]]

# ------------------------------
# Functions
# ------------------------------

# Convert a set of deviation pairs to radial symmetry
def radial(coordSet):
    if len(coordSet) % 2 == 0:
        print('There must be an odd number of deviation coordinates to make a mutation with radial symmetry')
    else:
        symmetryPairs = []
        negSymmetryPairs = []
        for pair in coordSet:
            negDeviationPair = [pair[0] * -1, pair[1] * -1]
            if pair != [0,0] and pair not in symmetryPairs and pair not in negSymmetryPairs:
                symmetryPairs.append(pair)
                negSymmetryPairs.append(negDeviationPair)
                if len(symmetryPairs) >= (len(coordSet) - 1) / 2:
                    break
        negSymmetryPairs.reverse()
        symmetryPairs.append([0,0])
        for j in range(len(negSymmetryPairs)):
            symmetryPairs.append(negSymmetryPairs[j])
        return symmetryPairs

# Divide a list of deviation pairs into rows
def makeRows(pairList):
    rowList = []
    row = []
    for i in range(len(pairList)):
        row.append(pairList[i])
        if len(row) == grid + 1:
            rowList.append(row.copy())
            row = []
    return rowList

# Generate a mutation based on a list of rows of deviation pairs
def mutation(rowList):
    newPage(canvasW,canvasH)
    cmykFill(0,0,0,0)
    rect(0,0,canvasW,canvasH)
    cmykFill(None)
    lineJoin('round')
    lineCap('round')

    if displayGrid:
        cmykStroke(0,0,0,0.8)
        for i in range((grid * subgrid) + (deviationMax * 2) + (marginW * 2)):
            line( (0, i * subgridUnit), (canvasW, i * subgridUnit) )
            line( (i * subgridUnit, 0), (i * subgridUnit, canvasH) )
        strokeWidth(weight * 2)
        for i in range(grid + 1):
            line( (margin, margin + (gridUnit * i)), (margin + (gridUnit * grid), margin + (gridUnit * i)) )
            line( (margin + (gridUnit * i), margin), (margin + (gridUnit * i), margin + (gridUnit * grid)) )
    
    cmykStroke(0,0,0,1)
    strokeWidth(weight)
    
    mutationRows = []
    for i in range(grid):
        for j in range(density + 1):
            if i == grid - 1 or (i < grid - 1 and j < density):
                thisRow = rowList[i]
                nextRow = rowList[i+1]
                mutationRows.append([])
                for k in range(grid + 1):
                    x1 = margin + (subgridUnit * thisRow[k][0]) + (gridUnit * k)
                    y1 = canvasH - (margin + (subgridUnit * thisRow[k][1]) + (gridUnit * i))
                    x2 = margin + (subgridUnit * nextRow[k][0]) + (gridUnit * k)
                    y2 = canvasH - (margin + (subgridUnit * nextRow[k][1]) + (gridUnit * (i+1)))
                    if fileType == 'svg':
                        y1 = (margin + (subgridUnit * thisRow[k][1]) + (gridUnit * i))
                        y2 = (margin + (subgridUnit * nextRow[k][1]) + (gridUnit * (i+1)))
                    x  = x1 + (((x2 - x1) / density) * j)
                    y  = y1 + (((y2 - y1) / density) * j)
                    mutationRows[-1].append((x,y))
    rowLoop = 1
    waves = BezierPath()
    svgData = '<figure class="gallery__item" id="' + fileNamePrefix.lower() + str(mutationID).zfill(2) + '"><svg width="' + str(canvasW) + '" height="' + str(canvasH) + '" viewBox="0 0 ' + str(canvasW) + ' ' + str(canvasH) + '"><rect width="' + str(canvasW) + '" height="' + str(canvasH) + '" fill="#fff"/><path fill="none" stroke="#000" stroke-width="' + str(weight).zfill(1) + '" stroke-linecap="round" d="'
    for i in range(len(mutationRows)):
        for j in range(len(mutationRows[i])):
            if j == 0:
                waves.moveTo(mutationRows[i][j])
                svgData += 'M' + str(round(mutationRows[i][j][0], 2)) + ' ' + str(round(mutationRows[i][j][1], 2)) + ' '
            else:
                xDif = mutationRows[i][j][0] - mutationRows[i][j-1][0]
                xDifUnit = xDif / 4
                ctrlX = (xDifUnit * ((density - rowLoop) / density)) + xDifUnit
                if rowLoop >= density / 2:
                    ctrlX = (xDifUnit * (rowLoop/density)) + xDifUnit
                waves.curveTo((mutationRows[i][j-1][0] + ctrlX, mutationRows[i][j-1][1]), (mutationRows[i][j][0] - ctrlX, mutationRows[i][j][1]), mutationRows[i][j])
                svgData += 'C' + str(round(mutationRows[i][j-1][0] + ctrlX, 2)) + ' ' + str(round(mutationRows[i][j-1][1], 2)) + ',' + str(round(mutationRows[i][j][0] - ctrlX, 2)) + ' ' + str(round(mutationRows[i][j][1], 2)) + ', ' + str(round(mutationRows[i][j][0], 2)) + ' ' + str(round(mutationRows[i][j][1], 2)) + ' '
        if rowLoop < density:
            rowLoop += 1
        else:
            rowLoop = 1
    if fileType == 'svg':
        print(svgData + '"/></svg><figcaption class="gallery__caption">' + fileNamePrefix + str(mutationID).zfill(2) + '</figcaption></figure>')
    drawPath(waves)


# ------------------------------
# Generate a Random Mutation
# ------------------------------

# random.shuffle(deviationPairs)

# # Asymmetrical
# mutation(makeRows(deviationPairs))

# # Symmetrical
# mutation(makeRows(radial(deviationPairs)))


# ------------------------------
# Generate Selected Mutations
# ------------------------------

for i in range(len(selections)):
    mutationID += 1
    mutation(makeRows(selections[i]))
    if fileType == 'pdf':
        saveImage(fileNamePrefix + str(mutationID).zfill(2) + '.' + fileType, multipage=False)


# ------------------------------
# Generate Average of Selected Mutations
# ------------------------------

# selectionsAvg = []
# for i in range(len(deviationPairs)):
#     selectionsAvg.append([0,0])
# for i in range(len(selections)):
#     for j in range(len(deviationPairs)):
#         selectionsAvg[j][0] += deviations.index(selections[i][j][0])
#         selectionsAvg[j][1] += deviations.index(selections[i][j][1])
# for i in range(len(selectionsAvg)):
#     selectionsAvg[i][0] = deviations[int(selectionsAvg[i][0] / len(selections))]
#     selectionsAvg[i][1] = deviations[int(selectionsAvg[i][1] / len(selections))]
    
# mutation(makeRows(selectionsAvg))