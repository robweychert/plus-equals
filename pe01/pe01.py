# Read Plus Equals #1 (https://plusequals.art/01) for the
# backstory on this script. Run the script in DrawBot
# (https://drawbot.com) to generate all 64 images shown in
# Plus Equals #1.


# ------------------------------------------------------------
# SETTINGS
# ------------------------------------------------------------

issue = 'PE01'

# `format` takes one of three settings: 'pdf', 'svg', or
# 'pdf svg' (to generate both). For 'pdf', a directory named
# 'Art' is created in the same directory as this script file
# and a PDF for each image is generated inside that directory.
# 'svg' generates the HTML I use to render the art on the Plus
# Equals site, using the SVG sprite system described here:
# https://css-tricks.com/svg-sprites-use-better-icon-fonts/
# I created the sprites themselves separately by drawing them
# in Adobe Illustrator and tweaking the SVG output.

format = ['pdf']
canvasWidth = 500
canvasHeight = canvasWidth
fgColor = (0,0,0) # Foreground color
bgColor = (1,1,1) # Background color


# ------------------------------------------------------------
# UTILITY FUNCTIONS
# ------------------------------------------------------------

# The cards are all drawn on a 28x28 grid, so the `unit`
# function is used to specify coordinates on that grid, and
# the coordinates will scale to whatever the canvas
# dimensions may be.

def unit(number):
    return number * (canvasWidth / 28)

def drawLine(x1,y1,x2,y2):
    newPath()
    stroke(*fgColor)
    strokeWidth((unit(1) / 3))
    lineCap('round')
    moveTo((x1,y1))
    lineTo((x2,y2))
    drawPath()

def rotateCard(card):
    with savedState():
        rotate(-90)
        translate(unit(-28))
        cards[cards.index(card)]()                       


# ------------------------------------------------------------
# CARD DRAWINGS
# ------------------------------------------------------------

# Draw Card A

def a():
    for i in range(3):
        fill(*bgColor)
        stroke(None)
        base = unit(20 - (i * 8))
        rect( 0, base, unit(28), unit(4) )
        for j in range(-3,28):
            if not j % 2 == 0:
                drawLine( unit(j), base, unit(j + 4), base + unit(4) )

# Draw Card B (which is Card A rotated 90º)

def b():
    rotateCard(a)

# Draw Card C

def c():
    for i in range(-11,14):
        if (i + 7) % 4 == 0:
            fill(*bgColor)
            stroke(None)
            polygon( (unit(i), unit(i * -1)), (unit(i - 2), unit((i * -1) + 2)), (unit(i + 26), unit((i * -1) + 30)), (unit(i + 28), unit((i * -1) + 28)) )
            for j in range(28):
                if not j % 2:
                    drawLine( unit(i + j), unit((i * -1) + j), unit(i + j), unit((i * -1) + j + 4) )

# Draw Card D (which is Card C rotated 90º)

def d():
    rotateCard(c)

cards = [a, b, c, d]
cardNames = ['A', 'B', 'C', 'D']

print(str(len(cards)) + " cards")


# ------------------------------------------------------------
# FIND ALL POSSIBLE COMBINATIONS
# ------------------------------------------------------------

# Calculate the number of ways the available cards
# can be combined

possibleCombos = 0

for i in range(len(cards)):
    possibleCombos = (possibleCombos + 1) * (i + 1)

print(str(possibleCombos) + " combos possible")

# In the `combos` list, make sublists of all possible
# card combinations

combos = []
prevCombos = []
currentCombos = []

for i in range(len(cards)):
    if i == 0:
        for card in cards:
            currentCombos.append([card])
    else:
        for combo in prevCombos:
            for card in cards:
                if len(currentCombos) == 0 or currentCombos[-1] != combo:
                    currentCombos.append(combo.copy())
                if card not in currentCombos[-1]:
                    currentCombos[-1].append(card)
    prevCombos = []
    for combo in currentCombos:
        if combo not in combos:
            prevCombos.append(combo.copy())
            combos.append(combo.copy())
    currentCombos = []

print(str(len(combos)) + " combos found")


# ------------------------------------------------------------
# DRAW THE COMBINATIONS
# ------------------------------------------------------------

# PDF filenames and/or HTML figure IDs for each image
# will be formatted like this: 'PE01-[card combination]'
# (e.g. 'PEO1-ABCD'). The HTML/SVG will look like this:
#
# <figure class="gallery__item" id="pe01-abcd">
#   <svg viewBox="0 0 252 252" width="252" height="252">
#     <use xlink:href="#card-bg"></use>
#     <use xlink:href="#a"></use>
#     <use xlink:href="#b"></use>
#     <use xlink:href="#c"></use>
#     <use xlink:href="#d"></use>
#   </svg>
#   <figcaption class="gallery__caption">PE01-ABCD</figcaption>
# </figure>

currentCombo = 0

for combo in combos:
    comboId = ''
    for card in combo:
        comboId = comboId + cardNames[cards.index(card)]
    comboId = issue + '-' + comboId
    if 'svg' in format:
        print('<figure class="gallery__item" id="' + comboId.lower() + '"><svg viewBox="0 0 252 252" width="252" height="252"><use xlink:href="#card-bg"></use>')
    if 'pdf' in format:
        newPage(canvasWidth,canvasHeight)
    for card in combo:
        if 'pdf' in format:
            card()
        if 'svg' in format:
            print('<use xlink:href="#' + cardNames[cards.index(card)].lower() + '"></use>')
    if 'svg' in format:
        print('</svg><figcaption class="gallery__caption">' + comboId + '</figcaption></figure>')
    if 'pdf' in format:
        currentCombo += 1
        import os
        if not os.path.exists('Art/'):
            os.makedirs('Art/')
        saveImage('Art/' + comboId + '.pdf', multipage=False)