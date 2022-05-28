from heapq import heapify, heappop, heappush
import sys
import numpy as np
from shapely.geometry import Point, LineString
from shapely.geometry.polygon import Polygon
import matplotlib as plt
from collections import defaultdict


# A* Search algorithm that uses nodes at only integer coordinates, path could be shorter if I made more nodes

file = open("navigate.in", "r")
sys.stdout = open("navigate.out", "w")
coords = []
for x in file.readlines():
    coords.append(tuple(int(i) for i in x.split()))



polygon = Polygon(coords[2:])
start = coords[0]
end = coords[1]

# heuristic for estimating distance from node to goal is a straight line

def h(start, goal):
    return np.linalg.norm(np.array(goal)-np.array(start))


def reconstruct_path(cameFrom, current):
    path = [current]
    while current in cameFrom:
        current = cameFrom[current]
        path.insert(0, current)
    return path


# each key value pair in cameFrom is what node, and where it came from
cameFrom = {}

# gScore[node] gives the best known path to that node
gScore = defaultdict(lambda: float("inf"))
gScore[start] = 0

# fScore[node] is the gScore plus the value from the h function
fScore = defaultdict(lambda: float("inf"))
fScore[start] = h(start, end)

# minheap sorted based off fScore
openSet = [(fScore[start], start)]
heapify(openSet)

while openSet:
    fS, current = heappop(openSet)

    # if there is an unobstructed straight line from the node to the goal, use it
    line = LineString([list(current),list(end)])
    if not line.intersects(polygon):
        cameFrom[end] = current
        current = end

    if current == end:
        last = np.array([0,0])
        for i in reconstruct_path(cameFrom, current)[1:]:
            print(*i)
            last = i
        break


    # check each of its neighbors to find which gives the best fScore
    for i in range(-1, 2):
        for j in range(-1, 2):

            neighbor = (current[0]+i, current[1]+j)
            if (i == 0 and j == 0) or polygon.contains(Point(neighbor[0], neighbor[1])):
                continue

            curG = gScore[current] + \
                np.linalg.norm(np.array(neighbor)-np.array(current))

            if curG < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = curG
                fScore[neighbor] = curG + h(neighbor, end)
                if not neighbor in openSet:
                    heappush(openSet, (fScore[neighbor], neighbor))
