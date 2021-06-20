# Read Plus Equals #2 (https://plusequals.art/02) for the
# backstory on this script. Run the script in DrawBot
# (https://drawbot.com) to generate all 720 images shown in
# Plus Equals #2.

# ------------------------------------------------------------
# SETTINGS
# ------------------------------------------------------------

issue = 'PE02'
image = u"pe02-george-floyd.gif" # Source image

# `generate` determines the content of the final output using
# the following values:
#
# 'art': generates the final art in the file format specified
# in `fileType`, in a directory named 'Art'. I use this to
# generate PDFs for the print edition.
# 
# 'index': generates a map of tone values for the canvas grid
# (stored in `imageTones`), in a directory named 'Index'
# 
# 'sprites': generates all the pieces (sprites) needed to
# assemble all of the final art's possible variations on the
# website, in a directory named 'Sprites', as well as printing
# corresponding SVG <defs> code. See the SVG sprite system
# described here:
# https://css-tricks.com/svg-sprites-use-better-icon-fonts/
#
# 'HTML': prints the SVG <use> code I use on the website in
# conjunction with the aforementioned <defs> to assemble all
# of the final art's variations on the website

generate = 'art' # art | index | sprites | html
# fileType = 'png' # pdf | svg | png | jpg | gif | etc

gridW = 54 # The canvas grid width
canvasW = 480 # The final art's pixel width

# `tones` is the final art's palette size. You can comment it
# out for the richest possible tonal range, but that will
# limit the output to one image.

tones = 6

# CAUTION: Setting `variations` to True can generate a number
# of images equal to the factorial of `tones`, which might be,
# you know, a LOT.

variations = False

# ------------------------------------------------------------
# ADDITIONAL VARIABLES
# ------------------------------------------------------------

imageW, imageH = imageSize(image)
gridH = int(gridW * (imageH / imageW))
canvasH = canvasW * (imageH / imageW)
canvasGrid = canvasW / gridW
imageGrid = imageW / gridW
toneValues = []
imageTones = []
combos = []

# On the website, each of the final art's variations is made
# of five sprites. One sprite includes all of the halftone
# dots corresponding to the second value in `toneValues`,
# another sprite includes all the dots corresponding to the
# third value, etc. (The first value is white, so it has no
# dots and is ignored.) When `gridLoop(draw)` is run,
# `spriteTone` represents the tone value of the current grid
# unit in `imageTones`, and `spriteToneVar` represents the
# the tone that takes its place in the current variation's
# tone sequence. So a sprite whose 2 palette value has been
# replaced with 4 would be encoded as 24.

spriteTone = 0
spriteToneVar = 0

drawing = 0

# ------------------------------------------------------------
# GENERATE THE PALETTE AND ALL POSSIBLE PALETTE SEQUENCES
# ------------------------------------------------------------

# This uses `tones` to determine the values of the palette's
# tones, add them to `toneValues`, and add every possible
# sequence of those tones to `combos`.

if 'tones' in globals():

    # Determine the values of the palette's tones and add them
    # to `toneValues`

    tones -= 1
    for i in range(tones):
        value = (1 / tones) * i
        toneValues.append(round(value, 3))
    toneValues.append(1)
    
    prevCombos = []
    currentCombos = []

    # In the `combos` list, make sublists of all possible
    # palette sequences

    for i in range(len(toneValues)):
        if i == 0:
            for j in range(len(toneValues)):
                currentCombos.append([j])
        else:
            for combo in prevCombos:
                for k in range(len(toneValues)):
                    if len(currentCombos) == 0 or currentCombos[-1] != combo:
                        currentCombos.append(combo.copy())
                    if k not in currentCombos[-1]:
                        currentCombos[-1].append(k)
        prevCombos = []
        for combo in currentCombos:
            if combo not in combos:
                prevCombos.append(combo.copy())
                if len(combo) == len(toneValues):
                    combos.append(combo.copy())
        currentCombos = []

combos.sort()

# ------------------------------------------------------------
# MAP THE SOURCE IMAGE AND DRAW THE ART
# ------------------------------------------------------------

# When set to 'map', `gridLoop` scans the source image and
# maps the palette tone for each of the final art's grid
# units. When set to 'draw', it will generate the final art
# and/or website code according to the editable `generate` and
# `fileType` settings at the top of the file.

def gridLoop(task):
    if task == 'draw' and ((variations and 'tones' in globals() and generate == 'sprites') or (generate != 'html')):
        newPage(canvasW,canvasH)
    dot = 0 # The current grid unit in `imageTones`
    # Loop through each unit of the canvas grid
    for x in range(gridW):
        for y in range(gridH):
            # If the x coordinate is even and the y coordinate is odd,
            # or vice versa (this creates a checkerboard pattern)
            if (x + y) % 2 != 0:
                if task == 'map':
                    # Find the pixel in the source image that corresponds
                    # with the current canvas grid unit, capture its color
                    # value, and convert it to grayscale
                    color = imagePixelColor(image,((imageGrid * x) + (imageGrid / 2), (imageGrid * y) + (imageGrid / 2)))
                    tone = round((1 - ((color[0] + color[1] + color[2]) / 3)), 3)
                    if 'tones' in globals():
                        global tones
                        toneInterval = (toneValues[1] - toneValues[0]) / 2
                        # Find the palette tone value closest to the current
                        # pixel's grayscale value and make that the current tone
                        for i in range(len(toneValues)):
                            if tone >= (toneValues[i] - toneInterval) and tone <= (toneValues[i] + toneInterval):
                                tone = toneValues[i]
                                break
                        # Add the current tone to the map
                        imageTones.append(round(tone, 3))
                    else:
                        imageTones.append(tone)
                if task == 'draw':
                    tone = imageTones[dot]
                    if generate != 'html':
                        if 'tones' in globals():
                            if generate != 'sprites':
                                # Map the current tone to the current variation's
                                # palette sequence
                                global drawing
                                toneIndex = toneValues.index(tone)
                                currentCombo = combos[drawing]
                                comboIndex = currentCombo[toneIndex]
                                tone = toneValues[comboIndex]
                        if generate == 'index':
                            fontSize(canvasGrid)
                            text(str(toneValues.index(tone)), (canvasGrid * x + canvasGrid / 2, canvasGrid * y + canvasGrid / 8), align='center')
                        elif (variations and 'tones' in globals() and generate == 'sprites' and tone == toneValues[spriteTone]) or (generate != 'sprites' and tone > 0):
                            if generate == 'sprites':
                                tone = toneValues[spriteToneVar]
                                # The sprites were originally made of pure SVG, but their
                                # complexity caused some real performance problems on the
                                # site. The following line, commented out here for posterity,
                                # generates that SVG.
                                # print('<circle cx="' + str(round((x * canvasGrid + canvasGrid / 2), 2)) + '" cy="' + str(round((canvasH - (y * canvasGrid + canvasGrid / 2)), 2)) + '" r="' + str(round((canvasGrid * toneValues[spriteToneVar]), 2)) + '"/>')
                            # `gridOffset` keeps the halftone dot centered in its grid unit
                            gridOffset = (canvasGrid - (canvasGrid * tone * 2)) / 2
                            oval((canvasGrid * x) + gridOffset, (canvasGrid * y) + gridOffset, canvasGrid * 2 * tone, canvasGrid * 2 * tone)
                dot += 1
    if task == 'draw':
        filename = issue
        if 'cover' in image:
            filename += 'cover-'
        if generate == 'index':
            filename += 'index'
        elif generate == 'sprites':
            filename = filename.lower() + 'sprite-' + str(spriteTone) + str(spriteToneVar)
        elif 'tones' in globals():
            for i in range(len(combos[drawing])):
                thisDrawing = combos[drawing]
                filename += str(thisDrawing[i])
        if generate == 'html':
            # Sample generated gallery HTML/SVG:
            # <figure class="gallery__item" id="pe02-012345">
            #   <svg viewBox="0 0 480 480" width="480" height="480">
            #     <use xlink:href="#card-bg"></use>
            #     <use xlink:href="#11"></use>
            #     <use xlink:href="#22"></use>
            #     <use xlink:href="#33"></use>
            #     <use xlink:href="#44"></use>
            #     <use xlink:href="#55"></use>
            #   </svg>
            #   <figcaption class="gallery__caption">PE02-012345</figcaption>
            #  </figure>
            print('<figure class="gallery__item" id="' + filename.lower() + '"><svg viewBox="0 0 300 300" width="300" height="300"><use xlink:href="#card-bg"></use>')
            for i in range(len(combos[drawing])):
                thisDrawing = combos[drawing]
                if thisDrawing[i] > 0:
                    print('<use xlink:href="#' + str(i) + str(thisDrawing[i]) + '"></use>')
            print('</svg><figcaption class="gallery__caption">' + str(filename) + '</figcaption></figure>')
        if 'fileType' in globals() and (generate != 'html'):
            directory = 'Art/'
            if generate == 'index':
                directory = 'Index/'
            elif generate == 'sprites':
                directory = 'Sprites/'
            import os
            if not os.path.exists(directory):
                os.makedirs(directory)
            saveImage(directory + filename + '.' + fileType, multipage=False)
        drawing += 1

# ------------------------------------------------------------
# 
# ------------------------------------------------------------

gridLoop('map')
if generate == 'sprites':
    for i in range(len(toneValues)):
        for j in range(len(toneValues)):
            if spriteToneVar > 0:
                # Sameple generated sprite SVG:
                # <g id="01"><image width="480" height="480.0" xlink:href="/assets/images/pe02-sprite-24.png"/></g>
                print('<g id="' + str(spriteTone) + str(spriteToneVar) + '">')
                gridLoop('draw')
                print('<image width="' + str(canvasW) + '" height="' + str(canvasH) + '" xlink:href="/assets/images/pe02-sprite-' + str(spriteTone) + str(spriteToneVar) + '.' + fileType + '"></image>')
                print('</g>')
            spriteToneVar += 1
        spriteTone += 1
        spriteToneVar = 0
elif 'tones' in globals() and variations:
    for i in combos:
        gridLoop('draw')
else:
    gridLoop('draw')