# Read Plus Equals #3 (https://plusequals.art/03) for the
# backstory on this script. Run the script in DrawBot
# (https://drawbot.com) to generate all 425 images shown in
# Plus Equals #3.

# ------------------------------------------------------------
# Settings (I may eventually modify this script to work with
# different grid settings, but for now it only works with a
# 3x3 grid)

gridW = 3
gridH = 3
version = 'poster' # '1up' | '9up' | 'poster' | 'svg'

# ------------------------------------------------------------
# Automatic dimensional variables

canvasW = 60
lineThickness = ((60/48) * 1.5)
if version == 'svg':
    canvasW = 96
    lineThickness = 3
if version == '9up':
    canvasW = 67.2
    lineThickness = ((67.2/48) * 1.5)
if version == 'poster':
    canvasW = 96
    lineThickness = 3
canvasH = int((gridH / gridW) * canvasW)
gridUnit = canvasW / gridW
posterW = canvasW * 25
posterH = canvasH * 17

# ------------------------------------------------------------
# Map the coordinates of all grid intersections

intersections = []

currentIntersection = []
for x in range(gridW + 1):
    for y in range(gridH + 1):
        currentIntersection.append(x)
        currentIntersection.append(y)
        intersections.append(currentIntersection)
        currentIntersection = []

print(str(len(intersections)) + ' intersections')

# ------------------------------------------------------------
# Identify the intersections on the perimeter of the grid and
# make them points

pointAmount = (gridW * 2) + (gridH * 2)
points = []

for intersection in intersections:
    if ((intersections.index(intersection) < gridW + 1) or (intersections.index(intersection) > (len(intersections) - (gridW + 1)))) or ((intersection[1] == 0) or (intersection[1] == gridW)):
        points.append(intersection)

print(str(len(points)) + ' points')

# ------------------------------------------------------------
# Put the points in lists of rows

rows = []
currentRow = []

for i in range(gridH + 1):
    for point in points:
        if point[1] == i:
            currentRow.append(point)
    rows.append(currentRow)
    currentRow = []

print(str(len(rows)) + ' rows')
# print(rows)

# ------------------------------------------------------------
# Put the points in lists of columns

cols = []
currentCol = []

for i in range(gridW + 1):
    for point in points:
        if point[0] == i:
            currentCol.append(point)
    cols.append(currentCol)
    currentCol = []

print(str(len(cols)) + ' columns')

# ------------------------------------------------------------
# Using the row and column lists, make a list of all unique
# point pairs that make diagonal lines

lineAmount = pointAmount / 2
lines = []

currentLine = []
for point1 in points:
    point1Row = []
    point1Col = []
    for row in rows:
        if point1 in row:
            point1Row = row
            break
    for col in cols:
        if point1 in col:
            point1Col = col
            break
    for point2 in points:
        if point2 != point1 and point2 not in point1Row and point2 not in point1Col:
            currentLine.append(point1)
            currentLine.append(point2)
            currentLine.sort()
            if currentLine not in lines:
                lines.append(currentLine)
            currentLine = []

print(str(len(lines)) + ' diagonal lines')
print(lines)

# ------------------------------------------------------------
# Sort the lines into two separate lists according to their
# initial point. In the first list, for each point in the
# grid's first column, make a sublist of relevant lines. Put
# all additional lines in the second list.

lines1stCol = []
lines1stColTotal = 0
linesAdditional = []

for line1 in lines:
    line1Start = line1[0]
    if line1Start[0] == 0:
        if len(lines1stCol) == 0:
            lines1stCol.append([line1])
            lines1stColTotal += 1
        else:
            for row in lines1stCol:
                line2 = row[0]
                linePresent = False
                if line1[0] == line2[0]:
                    row.append(line1)
                    linePresent = True
                    lines1stColTotal += 1
                    break
            if not linePresent:
                lines1stCol.append([line1])
                lines1stColTotal += 1
    else:
        linesAdditional.append(line1)

print(str(lines1stColTotal) + ' first-column lines in ' + str(len(lines1stCol)) + ' sublists')
print(str(len(linesAdditional)) + ' additional lines')

# ------------------------------------------------------------
# Find all possible unique line combinations of one line from
# each of the first-column sublists. No combination may
# include any repeated points.

combos1stCol = []

for sort in lines1stCol:
    combos1stCol.append([])
for i in range(len(lines1stCol)):
    for line1 in lines1stCol[i]:
        if i == 0:
            combos1stCol[i].append(line1)
        else:
            prev = combos1stCol[i - 1]
            current = combos1stCol[i]
            for combo in prev:
                current.append(combo.copy())
                comboSet = []
                for point in combo:
                    comboSet.append(str(point))
                for point in line1:
                    current[-1].append(point)
                    comboSet.append(str(point))
                if len(current[-1]) != len(set(comboSet)):
                    del current[-1]
combos1stCol = combos1stCol[-1]
combos1stCol.sort()

print(str(len(combos1stCol)) + ' first-column combos')

# ------------------------------------------------------------
# Find all possible unique combinations of lines from the list
# of additional lines. No combination may include any repeated
# points. All combos of additional lines should have the same
# number of lines, determined by the size of the first-column
# line combos. Example: a 3x3 grid can accommodate six lines
# total and four of them originate in first column; therefore,
# additional line combos for a 3x3 grid should include exactly
# two lines.

lineRemainder = int((len(points) / 2) - len(lines1stCol))
combosAdditional = []
scratchpad1 = []
scratchpad2 = []

if lineRemainder > 1:
    for i in range(lineRemainder):
        if i == 0:
            scratchpad2 = linesAdditional
        else:
            scratchpad1 = scratchpad2
            scratchpad2 = []
            for j in range(len(scratchpad1)):
                baseCombo = scratchpad1[j]
                baseLine = baseCombo[len(baseCombo) - 2 :: len(baseCombo) - 1]
                for k in range(linesAdditional.index(baseLine) + 1, len(linesAdditional)):
                    comboSet = []
                    scratchpad2.append([])
                    for point in scratchpad1[j]:
                        scratchpad2[-1].append(point)
                    for point in linesAdditional[k]:    
                        scratchpad2[-1].append(point)
                    for point in scratchpad2[-1]:
                        comboSet.append(str(point))
                    if len(scratchpad2[-1]) != len(set(comboSet)):
                        del scratchpad2[-1]
    combosAdditional = scratchpad2
    scratchpad1 = []
    scratchpad2 = []
else:
    combosAdditional = linesAdditional

print(str(len(combosAdditional)) + ' additional combos')

# ------------------------------------------------------------
# Find all possible unique combinations of first-column combos
# and additional line combos. No combination may include any
# repeated points.

combosFinal = []
scratchpad = []

for combo1stCol in combos1stCol:
    for comboAdditional in combosAdditional:
        comboSet = []
        for point in combo1stCol:
            scratchpad.append(point)
        for point in comboAdditional:
            scratchpad.append(point)
        for point in scratchpad:
            comboSet.append(str(point))
        if len(scratchpad) == len(set(comboSet)):
            combosFinal.append(scratchpad)
        scratchpad = []
combosFinal.sort()

print(str(len(combosFinal)) + ' final combos')

# ------------------------------------------------------------
# Draw the final combinations

def drawCombo(drawing):
    if version == 'svg':
        print('<g id="t' + str(combosFinal.index(combo) + 1).zfill(3) + '">')
    for point in range(int(len(drawing) / 2)):
        lineStart = drawing[point * 2]
        lineEnd = drawing[(point * 2) + 1]
        x1 = lineStart[0]
        y1 = lineStart[1]
        x2 = lineEnd[0]
        y2 = lineEnd[1]
        if version == 'svg':
            thisLine = [[x1, y1], [x2, y2]]
            print('<use xlink:href="#l' + str(lines.index(thisLine) + 1).zfill(2) + '"></use>')
        else:
            line((x1 * gridUnit, y1 * gridUnit), (x2 * gridUnit, y2 * gridUnit))
    if version == 'svg':
        print('</g>')

if version == 'svg':
    print('<!-- Line sprites -->')
    for i in range(len(lines)):
        thisLine = lines[i]
        point1 = thisLine[0]
        point2 = thisLine[1]
        print('<g id="l' + str(i + 1).zfill(2) + '"><line fill="none" stroke="#000" stroke-width="' + str(lineThickness) + '" stroke-linecap="round" x1="' + str(int(gridUnit * point1[0])) + '" y1="' + str(int(canvasH - (gridUnit * point1[1]))) + '" x2="' + str(int(gridUnit * point2[0])) + '" y2="' + str(int(canvasH - (gridUnit * point2[1]))) + '" /></g>')
    print('<!-- Tile sprites -->')
    for combo in combosFinal:
        drawCombo(combo)
    print('<!-- Gallery HTML -->')
    for i in range(len(combosFinal)):
        tileID = str(i + 1).zfill(3)
        svgOpen = '<svg viewbox="0 0 ' + str(canvasW) + ' ' + str(canvasH) + '">'
        def thisTile(transformX, transformY, gray):
            opacity = ''
            if gray == 1:
                opacity = ' opacity="0.333"'
            if transformX == 0 and transformY == 0 and gray == 0:
                return '<use xlink:href="#t' + tileID + '"' + opacity + '></use>'
            else:
                return '<use xlink:href="#t' + tileID + '"' + opacity + ' transform="translate(' + str(int(transformX * gridUnit)) + ' ' + str(int(transformY * gridUnit)) + ') scale(0.333)"></use>'
        print('<figure class="gallery__item" id="pe03-' + tileID + '">' + svgOpen + thisTile(0,0,0) + '</svg>' + svgOpen + thisTile(0,0,1) + thisTile(1,0,1) + thisTile(2,0,1) + thisTile(0,1,1) + thisTile(1,1,0) + thisTile(2,1,1) + thisTile(0,2,1) + thisTile(1,2,1) + thisTile(2,2,1) + '</svg><figcaption class="gallery__caption">PE03-' + tileID + '</figcaption></figure>')
elif version == 'poster':
    print('<svg viewbox="0 0 ' + str(posterW) + ' ' + str(posterH) + '">')
    newPage(posterW, posterH)
    x = 0
    y = 0
    course = 'down'
    for combo in combosFinal:
        with savedState():
            translate(x,y)
            lineCap('round')
            cmykStroke(0,0,0,1)
            strokeWidth(lineThickness)
            drawCombo(combo)
            print('<use xlink:href="#t' + str(int(combosFinal.index(combo) + 1)).zfill(3) + '" transform="translate(' + str(x) + ' ' + str(posterH - y - canvasH) + ')"></use>')
        for i in range(2):
            if course == 'down':
                if x == posterW - canvasW:
                    y = y + canvasH
                    course = 'up'
                    break
                elif y == 0:
                    x = x + canvasW
                    course = 'up'
                    break
                else:
                    x = x + canvasW
                    y = y - canvasH
                    break
            if course == 'up':
                if y == posterH - canvasH:
                    x = x + canvasW
                    course = 'down'
                    break
                elif x == 0:
                    y = y + canvasH
                    course = 'down'
                    break
                else:
                    x = x - canvasW
                    y = y + canvasW
                    break
    import os
    if not os.path.exists('Art/'):
        os.makedirs('Art/')
    saveImage('Art/PE03-poster.pdf', multipage=False)
    print('</svg>')
else:
    for combo in combosFinal:
        newPage(canvasW,canvasH)
        if version == '9up':
            xy = [-canvasW,canvasH,0,canvasH,canvasW,canvasH,-canvasW,0,canvasW,-canvasW,canvasW,0,-canvasW,-canvasW,0,-canvasW,0,0]
            for i in range(9):
                with savedState():
                    scale(1/3, center=(canvasW / 2, canvasH / 2))
                    translate(xy[i*2],xy[i*2+1])
                    lineCap('round')
                    cmykStroke(0,0,0,0.333333)
                    strokeWidth(lineThickness)
                    if i == 8:
                        cmykStroke(0,0,0,1)
                    drawCombo(combo)
            import os
            if not os.path.exists('Art/9up/'):
                os.makedirs('Art/9up/')
            saveImage('Art/9up/PE03-9up-' + str(combosFinal.index(combo) + 1).zfill(3) + '.pdf', multipage=False)
        else:
            with savedState():
                scale(48/60, center=(canvasW / 2, canvasH / 2))
                lineCap('round')
                cmykStroke(0,0,0,1)
                strokeWidth(lineThickness)
                drawCombo(combo)
            import os
            if not os.path.exists('Art/1up/'):
                os.makedirs('Art/1up/')
            saveImage('Art/1up/PE03-' + str(combosFinal.index(combo) + 1).zfill(3) + '.pdf', multipage=False)