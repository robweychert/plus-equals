# Read Plus Equals #4 (https://plusequals.art/04) for the
# backstory on this script. Run the script in DrawBot
# (https://drawbot.com) to generate all 252 images shown in
# Plus Equals #4.

#--------------------------------------------------
# Settings
#--------------------------------------------------

version = 'svg' # 'pdf' | 'svg' | 'pdf svg'

canvasW = 300 # Canvas width
canvasH = 300 # Canvas height
canvasP = (6/96) * canvasW # Canvas padding
areaW = 3     # 3D grid width
areaD = 3     # 3D grid depth
areaH = 3     # 3D grid height

axRatio = 1.732 # Axonometric ratio, x:1 (1.732:1 = isometric)

wFill = (0,0,0,0)
dFill = wFill
hFill = wFill
blockStroke = (0,0,0,1)
gridStroke = (0.25,0,0,0)
stroke = (2/96) * canvasW

#--------------------------------------------------
# Projected 3D grid measurements
#--------------------------------------------------

gridW = (areaW + areaD) * axRatio
gridH = (areaW + areaD) + (areaH * 2)
xUnit = 0
yUnit = 0
base = []

if gridW > gridH:
    xUnit = (canvasW - (canvasP * 2)) / (areaW + areaD)
    yUnit = xUnit / axRatio
    base.append(canvasP)
    base.append((areaW * yUnit) + ((canvasH - (gridH * yUnit)) / 2))
else:
    yUnit = (canvasH - (canvasP * 2)) / gridH
    xUnit = yUnit * axRatio
    base.append((canvasW - ((areaW + areaD) * xUnit)) / 2)
    base.append((areaW * yUnit) + canvasP)

#--------------------------------------------------
# Functions
#--------------------------------------------------

def drawGrid():
    for h in range(areaH + 1):
        for w in range(areaW):
            for d in range(areaD):
                fill(None)
                cmykStroke(*gridStroke)
                strokeWidth(stroke)
                lineJoin('round')
                cellBase = [ base[0] + (xUnit * d) + (xUnit * w),
                             base[1] + (yUnit * (h * 2)) - (yUnit * w) + (yUnit * d)]
                polygon( (cellBase[0], cellBase[1]),
                         (cellBase[0] + xUnit, cellBase[1]+ yUnit),
                         (cellBase[0] + (xUnit * 2), cellBase[1]),
                         (cellBase[0] + xUnit, cellBase[1] - yUnit),
                          close=True )

compoundPlanes = [[],[],[]]

def drawBlock(x,y,z,w,d,h,compound=False):
    blockBase = [base[0] + (xUnit * x) + (xUnit * y), base[1] - (yUnit * x) + (yUnit * y) + (yUnit * z * 2)]
    blockPoints = [
        [ # Width plane (left):
            [blockBase[0], blockBase[1]],
            [blockBase[0], blockBase[1] + (yUnit * 2 * h)],
            [blockBase[0] + (xUnit * w), blockBase[1] - (yUnit * w) + (yUnit * 2 * h)],
            [blockBase[0] + (xUnit * w), blockBase[1] - (yUnit * w)]
        ],
        [ # Depth plane (right):
            [blockBase[0] + (xUnit * w), blockBase[1] - (yUnit * w)],
            [blockBase[0] + (xUnit * w), blockBase[1] - (yUnit * w) + (yUnit * 2 * h)],
            [blockBase[0] + (xUnit * (w + d)), blockBase[1] - (yUnit * w) + (yUnit * d) + (yUnit * 2 * h)],
            [blockBase[0] + (xUnit * (w + d)), blockBase[1] - (yUnit * w) + (yUnit * d)]
        ],
        [ # Height plane (top):
            [blockBase[0], blockBase[1] + (yUnit * 2 * h)],
            [blockBase[0] + (xUnit * d), blockBase[1] + (yUnit * d) + (yUnit * 2 * h)],
            [blockBase[0] + (xUnit * (w + d)), blockBase[1] - (yUnit * w) + (yUnit * d) + (yUnit * 2 * h)],
            [blockBase[0] + (xUnit * w), blockBase[1] - (yUnit * w) + (yUnit * 2 * h)]
        ]
    ]
    if 'svg' in version and not spritesGenerated:
        if not compound:
            for plane in blockPoints:
                svgPolygon = '<polygon points="'
                for point in plane:
                    svgPolygon += str(round(point[0], 2)) + ','
                    svgPolygon += str(round(canvasH - point[1], 2)) + ' '
                svgPolygon += '" fill="#fff" stroke="#000" stroke-width="' + str(stroke) + '" stroke-linejoin="round" />'
                print(svgPolygon)
    wPlane = BezierPath()
    wPlane.polygon(
        (blockPoints[0][0][0], blockPoints[0][0][1]),
        (blockPoints[0][1][0], blockPoints[0][1][1]),
        (blockPoints[0][2][0], blockPoints[0][2][1]),
        (blockPoints[0][3][0], blockPoints[0][3][1]),
        close=True
    )
    dPlane = BezierPath()
    dPlane.polygon(
        (blockPoints[1][0][0], blockPoints[1][0][1]),
        (blockPoints[1][1][0], blockPoints[1][1][1]),
        (blockPoints[1][2][0], blockPoints[1][2][1]),
        (blockPoints[1][3][0], blockPoints[1][3][1]),
        close=True
    )
    hPlane = BezierPath()
    hPlane.polygon(
        (blockPoints[2][0][0], blockPoints[2][0][1]),
        (blockPoints[2][1][0], blockPoints[2][1][1]),
        (blockPoints[2][2][0], blockPoints[2][2][1]),
        (blockPoints[2][3][0], blockPoints[2][3][1]),
        close=True
    )
    if compound:
        compoundPlanes[0].append(wPlane)
        compoundPlanes[1].append(dPlane)
        compoundPlanes[2].append(hPlane)
    elif spritesGenerated:
        cmykStroke(*blockStroke)
        strokeWidth(stroke)
        lineJoin('round')
        cmykFill(*wFill)
        drawPath(wPlane)
        cmykFill(*dFill)
        drawPath(dPlane)
        cmykFill(*hFill)
        drawPath(hPlane)

#--------------------------------------------------
# Parts
#--------------------------------------------------
# The first set of numbers (in parentheses) defines
# the part's dimensions and coordinates for use
# with the drawBlock() function. The second set of
# numbers (in brackets) defines the numbered units
# of space the part occupies in the area where the
# parts will be arranged.

parts = [
    [ # 1x3
        [ (0,0,0,3,1,1), [1,2,3] ],
        [ (2,0,0,1,3,1), [3,4,5] ],
        [ (0,0,1,3,1,1), [6,7,8] ],
        [ (2,0,1,1,3,1), [8,9,10] ],
        [ (0,0,2,3,1,1), [11,12,13] ],
        [ (2,0,2,1,3,1), [13,14,15] ],
        [ (0,1,2,3,1,1), [14,16,17] ],
        [ (1,0,2,1,3,1), [12,17,18] ],
        [ (0,2,2,3,1,1), [15,18,19] ],
        [ (0,0,2,1,3,1), [11,16,19] ],
        [ (0,0,0,1,1,3), [1,6,11] ],
        [ (1,0,0,1,1,3), [2,7,12] ],
        [ (2,0,0,1,1,3), [3,8,13] ],
        [ (2,1,0,1,1,3), [4,9,14] ],
        [ (2,2,0,1,1,3), [5,10,15] ]
    ],
    [ # 2x2
        [ (0,0,0,2,1,2), [1,2,6,7] ],
        [ (1,0,0,2,1,2), [2,3,7,8] ],
        [ (2,0,0,1,2,2), [3,4,8,9] ],
        [ (2,1,0,1,2,2), [4,5,9,10] ],
        [ (0,0,1,2,1,2), [6,7,11,12] ],
        [ (1,0,1,2,1,2), [7,8,12,13] ],
        [ (2,0,1,1,2,2), [8,9,13,14] ],
        [ (2,1,1,1,2,2), [9,10,14,15] ],
        [ (0,0,2,2,2,1), [11,12,16,17] ],
        [ (1,0,2,2,2,1), [12,13,14,17] ],
        [ (1,1,2,2,2,1), [14,15,17,18] ],
        [ (0,1,2,2,2,1), [16,17,18,19] ]
    ],
    [ # 2x2x2
        [ [(0,0,1,2,1,2,True),(0,0,2,2,2,1,True)], [6,7,11,12,16,17] ],
        [ [(1,0,1,2,1,2,True),(1,0,2,2,2,1,True)], [7,8,12,13,14,17] ],
        [ [(2,0,1,1,2,2,True),(1,0,2,2,2,1,True)], [8,9,12,13,14,17] ],
        [ [(2,1,1,1,2,2,True),(1,1,2,2,2,1,True)], [9,10,14,15,17,18] ],
        [ [(1,0,0,2,1,2,True),(2,0,0,1,2,2,True)], [2,3,4,7,8,9] ],
        [ [(1,0,1,2,1,2,True),(2,0,1,1,2,2,True)], [7,8,9,12,13,14] ]
    ]
]

#--------------------------------------------------
# Generate SVG sprites for all parts
#--------------------------------------------------

spritesGenerated = False

for partSet in parts:
    for part in partSet:
        print('<g id="' + (str(chr(ord('@') + 1 + parts.index(partSet)))).lower() + str(partSet.index(part) + 1).zfill(2) + '">')
        if type(part[0]) != list:
            drawBlock(*part[0])
        else:
            for subPart in part[0]:
                drawBlock(*subPart)
            for i in range(len(part[0])):
                if i > 0:
                    compoundPlanes[0][0] = compoundPlanes[0][0].union(compoundPlanes[0][i])
                    compoundPlanes[1][0] = compoundPlanes[1][0].union(compoundPlanes[1][i])
                    compoundPlanes[2][0] = compoundPlanes[2][0].union(compoundPlanes[2][i])
            for plane in compoundPlanes:
                svgPolygon = '<polygon points="'
                for point in plane[0][0]:
                    svgPolygon += str(round(point[0][0], 2)) + ','
                    svgPolygon += str(round(canvasH - point[0][1], 2)) + ' '
                svgPolygon += '" fill="#fff" stroke="#000" stroke-width="' + str(stroke) + '" stroke-linejoin="round" />'
                print(svgPolygon)
            compoundPlanes = [[],[],[]]
        print('</g>')
            
spritesGenerated = True

#--------------------------------------------------
# Using one part from each set in `parts`, find all
# possible combinations of parts. Combos with parts
# that overlap in 3D space are disqualified.
#--------------------------------------------------

combos = []

for i in range(len(parts)):
    if i == 0:
        combos.append(parts[0].copy())
    else:
        combos.append([])
        for combo in combos[i - 1]:
            if i == 1:
                currentCombo = [combo.copy()]
            else:
                currentCombo = combo.copy()
            for part in parts[i]:
                partQualifies = True
                for area in part[1]:
                    for comboPart in currentCombo:
                        if area in comboPart[1]:
                            partQualifies = False
                if partQualifies:
                    currentCombo.append(part.copy())
                    combos[i].append(currentCombo)
                    if i == 1:
                        currentCombo = [combo.copy()]
                    else:
                        currentCombo = combo.copy()

print('combos: ' + str(len(combos[-1])))
                
#--------------------------------------------------
# Find all possible stacking orders for each combo
#--------------------------------------------------

stacks = []

import itertools
for combo in combos[-1]:
    sequences = list(itertools.permutations(combo, len(combo)))
    for sequence in sequences:
        stacks.append(sequence)

print('stacks: ' + str(len(stacks)))

#--------------------------------------------------
# Visual duplicates identified by eye from output
#--------------------------------------------------

duplicates = [2,6,16,17,22,23,33,36,39,42,50,54,57,60,70,71,76,77,81,84,86,90,104,108,116,120,128,132,135,138,141,144,146,150,166,167,172,173,182,186,189,192,195,198,208,209,214,215,220,221,225,228,232,233,243,246,248,252,260,264,266,270,285,288,292,293,298,299,303,306,314,318]

print('duplicates: ' + str(len(duplicates)))

#--------------------------------------------------
# Draw the stacks
#--------------------------------------------------

for stack in stacks:
    if (stacks.index(stack) + 1) not in duplicates:
        stackNumber = str(stacks.index(stack) + 1).zfill(3)
        stackID = ''
        stackParts = []
        newPage(canvasW,canvasH)
        # drawGrid()
        if 'pdf' in version:
            cmykFill(0,0,0,0,0)
            rect(0,0,canvasW,canvasH)
        cmykStroke(*blockStroke)
        strokeWidth(stroke)
        lineJoin('round')
        for part in stack:        
            for partSet in parts:
                if part in partSet:
                    partID = str(chr(ord('@') + 1 + parts.index(partSet))) + str(partSet.index(part) + 1).zfill(2)
                    stackParts.append(partID)
                    stackID = stackID + partID
            if type(part[0]) == list:
                for subPart in part[0]:
                    drawBlock(*subPart)
                for i in range(len(part[0])):
                    if i > 0:
                        compoundPlanes[0][0] = compoundPlanes[0][0].union(compoundPlanes[0][i])
                        compoundPlanes[1][0] = compoundPlanes[1][0].union(compoundPlanes[1][i])
                        compoundPlanes[2][0] = compoundPlanes[2][0].union(compoundPlanes[2][i])
                cmykFill(*wFill)
                drawPath(compoundPlanes[0][0])
                cmykFill(*dFill)
                drawPath(compoundPlanes[1][0])
                cmykFill(*hFill)
                drawPath(compoundPlanes[2][0])
                compoundPlanes = [[],[],[]]
            else:
                drawBlock(*part[0])
        if 'pdf' in version:
            import os
            if not os.path.exists('Art/'):
                os.makedirs('Art/')
            saveImage('Art/' + 'PE04-' + stackNumber + '-' + stackID + '.pdf', multipage=False)
        if 'svg' in version:
            print('<figure class="gallery__item" id="pe04-' + stackID.lower() + '"><svg viewbox="0 0 ' + str(canvasW) + ' ' + str(canvasH) + '" width="' + str(canvasW) + '" height="' + str(canvasH) + '">')
            for partID in stackParts:
                print('<use xlink:href="#' + str(partID).lower() + '"></use>')
            print('</svg><figcaption class="gallery__caption">' + 'PE04-' + stackID + '</figcaption></figure>')