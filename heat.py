import math as mt
import numpy as np
import os

def copy_mesh(mesh):
  os.chdir('mesh')
  os.system('cp ' + str(mesh) + ' ..')
  os.chdir('..')

def load_points_cells(filename):
  points = []
  cells = []
  pt_check = False
  cell_check = False
  with open(filename, 'r') as f:
    for line in f:
      text = line
      if 'POINTS' in text:
        pt_check = True
        continue
      elif 'CELLS' in text:
        cell_check = True
        continue
      elif text == '\n':
        pt_check = False
        cell_check = False
      else:
        pass
      
      if pt_check is True:
        points.append([float(n) for n in text.split()])
      elif cell_check is True:
        if text[0] == '4':
          cells.append([int(n) for n in text.split()])
      else:
        continue

  return points, cells

def calc_temp(x, y, z, t):
  ABS = 0.4
  P = 300
  K = 20
  V = 1.2
  A = 1e-4
  EPS = x - V*t
  r = mt.sqrt(EPS**2 + y**2 + z**2)

  T = 273 + ((ABS*P) / (2*mt.pi*K*r)) * mt.exp(-V*(r+EPS) / (2*A))

  return T

def simulate(points):

  T = np.zeros((len(points)))

  for i in range(len(points)):
    T[i] = calc_temp(points[i][0], points[i][1], points[i][2], 10e-5)

  return T

copy_mesh('untitled.vtk')

points, cells = load_points_cells('untitled.vtk')
T = simulate(points)

with open('untitled.vtk', 'a') as write_file:
  write_file.write('POINT_DATA ' + str(len(T)) + '\n')
  write_file.write('SCALARS Temperature float 1\n')
  write_file.write('LOOKUP_TABLE default\n')
  for i in range(len(T)):
    write_file.write('{T}\n'.format(T=T[i]))

print('\ndone')
