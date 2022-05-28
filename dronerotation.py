import numpy as np
import sys

sys.stdin = open("rotation.in","r")
sys.stdout = open("rotation.out","w")



pos_i = np.array([float(i) for i in input().split()])
drpy = [float(i) for i in input().split()]
dist, roll, pitch, yaw = drpy[0], drpy[1], drpy[2], drpy[3]


roll = np.radians(roll)
pitch = np.radians(pitch)
yaw = np.radians(yaw)

def calc_dir(r, p, y):
    r = -r
    Rx = np.array([[1, 0, 0],
                   [0, np.cos(p), -np.sin(p)],
                   [0, np.sin(p), np.cos(p)]])
    Ry = np.array([[np.cos(r), 0, np.sin(r)],
                   [ 0, 1, 0],
                   [-np.sin(r), 0, np.cos(r)]])
    Rz = np.array([[np.cos(y), -np.sin(y), 0],
                   [np.sin(y), np.cos(y), 0],
                   [0, 0, 1]])
    v = np.array([[0], [0], [1]])
    return (Rz @ Ry @ Rx @ v).reshape(-1)


disp_vec = calc_dir(roll, pitch, yaw) * dist
pos_f = pos_i + disp_vec
for i in pos_f:
  print(round(i,3),end=" ")
print()



