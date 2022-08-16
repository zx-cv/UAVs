from scipy.spatial import ConvexHull, convex_hull_plot_2d, distance
import numpy as np
import matplotlib.pyplot as plt
import math
import sys


# points = np.array([[0, 0], [1, 1], [2, 1.5], [3, 1], [4, 0], [
#                  2, -1], [3, -0.5], [3, -1]])

# read inputs
file = open("square.in", "r")
sys.stdout = open("square.out", "w")
points = []
for x in file.readlines():
    points.append([float(i) for i in x.split()])
points = np.array(points)
hull = ConvexHull(points)
x = 0
y = 0


# for vertex in hull.vertices:
#    plt.plot(points[vertex, 0], points[vertex, 1], 'bo')
#plt.plot(points[hull.vertices, 0], points[hull.vertices, 1], 'k-', lw=2)
# plt.plot(points[[hull.vertices[-1], hull.vertices[0]], 0],
#    points[[hull.vertices[-1], hull.vertices[0]], 1], 'k-', lw=2)

# Calculate centroid using formula shown here https://en.wikipedia.org/wiki/Centroid#Of_a_polygon
N = len(hull.vertices)
hv = hull.vertices
sum_Cx, sum_Cy = 0, 0
last_iteration = N-1
for i in range(N):
    if i != last_iteration:
        shoelace = points[hv[i], 0]*points[hv[i+1], 1] - \
            points[hv[i+1], 0]*points[hv[i], 1]
        sum_Cx += (points[hv[i], 0] + points[hv[i+1], 0]) * shoelace
        sum_Cy += (points[hv[i], 1] + points[hv[i+1], 1]) * shoelace
    else:
        # N-1 case (last iteration): substitute i+1 -> 0
        shoelace = points[hv[i], 0]*points[hv[0], 1] - \
            points[hv[0], 0]*points[hv[i], 1]
        sum_Cx += (points[hv[i], 0] + points[hv[0], 0]) * shoelace
        sum_Cy += (points[hv[i], 1] + points[hv[0], 1]) * shoelace
factor = 1 / (6*hull.volume)
Cx = factor * sum_Cx
Cy = factor * sum_Cy
p = np.array([Cx, Cy])
p2 = np.array([])
# plt.plot(Cx,Cy,'ro')

# Draw a line from the centroid to the furthest point on the hull that forms half the diagonal of the square
max = 0
for vertex in hull.vertices:
    dist = distance.euclidean(p, points[vertex])
    if dist > max:
        max = dist
        p2 = points[vertex]

area = ((2 * max)/math.sqrt(2)) ** 2
point1 = -(p2-p)+p
x1 = point1[0]
y1 = point1[1]
x2 = p2[0]
y2 = p2[1]

# solve for the rest of the points of the square
xc = (x1 + x2)/2
yc = (y1 + y2)/2
xd = (x1 - x2)/2
yd = (y1 - y2)/2

x3 = xc - yd
y3 = yc + xd
x4 = xc + yd
y4 = yc - xd

mp = (p2 + np.array([x3, y3]))/2
# plt.plot(mp[0],mp[1],'ro')

# use trig to find rotation
mpv = mp - p

print(*[np.round(area), np.round(np.degrees(np.arctan2(mpv[1], mpv[0])) % 90)])
# plt.plot(p[0],p[1],'ro')
# plt.plot(point1[0],point1[1],'ro')
# plt.plot(x3,y3,'ro')
# plt.plot(x4,y4,'ro')

# plt.show()
