# Read Plus Equals #6 (https://plusequals.art/06) for the
# backstory on this script. Run the script in DrawBot
# (https://drawbot.com) to generate all 562 images shown in
# Plus Equals #6.

#--------------------------------------------------
# Settings
#--------------------------------------------------

version = 'pdf svg' # 'pdf' | 'svg' | 'pdf svg'
canvasW = 300   # canvas width
gridW = 5       # grid width


# -------------------------------------------------
# Automatic dimensional variables
# -------------------------------------------------

canvasH = canvasW
gridH = gridW
gridUnit = canvasW / gridW

# -------------------------------------------------
# Functions
# -------------------------------------------------

def canvasCoord(gridCoord):
    return gridCoord * gridUnit

# -------------------------------------------------
# Map the grid intersections and find the center
# point (or the closest thing to it)
# -------------------------------------------------

points = []
for i in range(gridH):
    for j in range (gridW):
        if (i > 0) and (i < gridH) and (j > 0) and (j < gridW):
            points.append([j, i])
print(str(len(points)) + ' points')

centerPoint = []
if len(points) % 2 != 0:
    centerPoint = points[int(len(points) / 2)]
else:
    centerPoint = points[int((len(points) / 2) + (gridW / 2))]
print(str(centerPoint) + ' is the center point')


# -------------------------------------------------
# Find all possible sequences of points on the grid
# that begin from the center point. These will be
# the end points for a chain of Bézier curves.
# -------------------------------------------------

branches = []
branch = [centerPoint]
branchLastPoint = centerPoint
loopNextPoint = points[0]
backtrack = False

# While `branch` has at least one point in it
while len(branch) > 0:
    # Loop through the `points` list, beginning with `loopNextPoint`
    for point in points[points.index(loopNextPoint):]:
        xDif = abs(branchLastPoint[0] - point[0])
        yDif = abs(branchLastPoint[1] - point[1])
        # If the current point is the correct distance away from the branch's last point
        # and is not already somewhere else in the branch, the point qualifies for inclusion
        if ((xDif == 1 and yDif == 2) or (xDif == 2 and yDif == 1)) and (point not in branch):
            # Add the current point to the branch
            branch.append(point)
            # Make `branchLastPoint` the current point
            branchLastPoint = point
            # Move the loop position back to the first point
            loopNextPoint = points[0]
            backtrack = False
            # End the loop
            break
        # If the current point doesn't qualify for inclusion and is the last point in the loop
        elif points.index(point) == len(points) - 1:
            # If the branch is not backtracking
            if not backtrack:
                # Add the completed branch to the list of branches
                branches.append(branch.copy())
            # The branch is now backtracking
            backtrack = True
            # Record and remove the completed branch's endpoint
            branchEndPoint = branch[len(branch) - 1]
            del branch[len(branch) - 1]
            if len(branch) > 0:
                # Make `branchLastPoint` the branch's last point
                branchLastPoint = branch[len(branch) - 1]
                while points.index(branchEndPoint) == len(points) - 1 and len(branch) > 0:
                    # Record and remove the completed branch's endpoint
                    branchEndPoint = branch[len(branch) - 1]
                    del branch[len(branch) - 1]
                    # Make `branchLastPoint` the branch's last point
                if len(branch) > 0:
                    branchLastPoint = branch[len(branch) - 1]
                    loopNextPoint = points[points.index(branchEndPoint) + 1]

branchesByLength = []
branchNine = []
for branch in branches:
    branchesByLength.append(len(branch))
    if len(branch) == 9:
        branchNine.append(branch)
branchesByLength.sort()
print(str(len(branchNine)) + ' nine-point branches')
            
print(str(len(branchesByLength)) + ' branches')
print(str(branchesByLength[0]) + ' points in the shortest branch')
print(str(branchesByLength[len(branchesByLength) - 1]) + ' points in the longest branch')

# # -------------------------------------------------
# # Directional cycles for the control points
# # -------------------------------------------------

# angleOrders = [
#     ['h','v','d','v'],
#     ['v','h','d','h'],
#     ['d','h','v','h'],
#     ['h','d','v','d'],
#     ['v','d','h','d'],
#     ['d','v','h','v']
# ]
# angleOrder = 0
# angle = 0

# # -------------------------------------------------
# # Draw the scribbles
# # -------------------------------------------------

# branches.sort()

# for branch in branches:
#     branchId = 'pe06-' + str(branches.index(branch) + 1).zfill(3)
    
#     newPage(canvasW,canvasH)
#     cmykFill(0,0,0,0)
#     rect(0,0,canvasW,canvasH)
    
#     if version == 'svg' or version == 'pdf svg':
#         print('<figure class="gallery__item" id="' + branchId + '"><svg width="' + str(canvasW) + '" height="' + str(canvasH) + '" viewBox="0 0 ' + str(canvasW) + ' ' + str(canvasH) + '"><rect width="' + str(canvasW) + '" height="' + str(canvasH) + '" fill="white"/><path fill="none" stroke="black" stroke-width="' + str(int(gridUnit / 15)) + '" stroke-linecap="round" d="')

#     path = newPath()
#     moveTo((canvasCoord(centerPoint[0]), canvasCoord(centerPoint[1])))
    
#     if version == 'svg' or version == 'pdf svg':
#         print('M ' + str(int(canvasCoord(centerPoint[0]))) + ' ' + str(int(canvasH - canvasCoord(centerPoint[1]))) + ' ')
        
#     prevControl2 = None
#     for point in branch:
#         pointX = canvasCoord(point[0])
#         pointY = canvasCoord(point[1])
#         if branch.index(point) > 0:
#             if version == 'svg' or version == 'pdf svg':
#                 print('C ')
#             prevPointX = canvasCoord(branch[branch.index(point) - 1][0])
#             prevPointY = canvasCoord(branch[branch.index(point) - 1][1])
#             prevAngle = angleOrders[angleOrder][angle - 1]
            
#             # The position of control points is determined by their angle
#             # and the position of the previous end point
            
#             if prevPointX < pointX:
#                 if prevPointY < pointY:
#                     prevPointDir = ['n','w']
#                 else:
#                     prevPointDir = ['s','w']
#             elif prevPointY < pointY:
#                 prevPointDir = ['n','e']
#             else:
#                 prevPointDir = ['s','e']
                
#             if prevControl2:
#                 control1X = prevPointX + (prevPointX - prevControl2[0])
#                 control1Y = prevPointY + (prevPointY - prevControl2[1])
#             else:
#                 if prevAngle == 'h':
#                     control1Y = prevPointY
#                     if prevPointDir[1] == 'w':
#                         control1X = prevPointX + gridUnit
#                     else:
#                         control1X = prevPointX - gridUnit
#                 elif prevAngle == 'v':
#                     control1X = prevPointX
#                     if prevPointDir[0] == 'n':
#                         control1Y = prevPointY + gridUnit
#                     else:
#                         control1Y = prevPointY - gridUnit
#                 elif prevAngle == 'd':
#                     if prevPointDir[1] == 'w':
#                         control1X = prevPointX + gridUnit
#                         if prevPointDir[0] == 'n':
#                             control1Y = prevPointY + gridUnit
#                         else:
#                             control1Y = prevPointY - gridUnit
#                     else:
#                         control1X = prevPointX - gridUnit
#                         if prevPointDir[0] == 'n':
#                             control1Y = prevPointY + gridUnit
#                         else:
#                             control1Y = prevPointY - gridUnit
#             control1 = (control1X, control1Y)
#             if version == 'svg' or version == 'pdf svg':
#                 print(str(int(control1X)) + ' ' + str(int(canvasH - control1Y)) + ', ')
                
#             if angleOrders[angleOrder][angle] == 'h':
#                 control2Y = pointY
#                 if prevPointDir[1] == 'w':
#                     control2X = pointX - gridUnit
#                 else:
#                     control2X = pointX + gridUnit
#             elif angleOrders[angleOrder][angle] == 'v':
#                 control2X = pointX
#                 if prevPointDir[0] == 'n':
#                     control2Y = pointY - gridUnit
#                 else:
#                     control2Y = pointY + gridUnit
#             elif angleOrders[angleOrder][angle] == 'd':
#                 if prevPointDir[1] == 'w':
#                     control2X = pointX - gridUnit
#                     if prevPointDir[0] == 'n':
#                         control2Y = pointY - gridUnit
#                     else:
#                         control2Y = pointY + gridUnit
#                 else:
#                     control2X = pointX + gridUnit
#                     if prevPointDir[0] == 'n':
#                         control2Y = pointY - gridUnit
#                     else:
#                         control2Y = pointY + gridUnit
#             control2 = (control2X, control2Y)
#             if version == 'svg' or version == 'pdf svg':
#                 print(str(int(control2X)) + ' ' + str(int(canvasH - control2Y)) + ', ' + str(int(pointX)) + ' ' + str(int(canvasH - pointY)))
            
#             curveTo(control1, control2, (pointX, pointY))
#             prevControl2 = control2
            
#         if angle == len(angleOrders[angleOrder]) - 1:
#             angle = 0
#         else:
#             angle += 1
            
#     angle = 0
#     cmykFill(None)
#     cmykStroke(0,0,0,100)
#     strokeWidth(gridUnit / 15)
#     lineCap('round')
#     lineJoin('round')
#     drawPath(path)
#     if angleOrder == len(angleOrders) - 1:
#         angleOrder = 0
#     else:
#         angleOrder += 1
    
#     if version == 'svg' or version == 'pdf svg':
#         print('"/></svg><figcaption class="gallery__caption">' + branchId.upper() + '</figcaption></figure>')
#     if version == 'pdf' or version == 'pdf svg':
#         import os
#         if not os.path.exists('Art/'):
#             os.makedirs('Art/')
#         saveImage('Art/' + branchId.upper() + '.pdf', multipage=False)