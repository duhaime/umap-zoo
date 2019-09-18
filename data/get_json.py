# process results from distribute.py into web form

import glob, vertices, json, os
import numpy as np

def rotate(X, theta, axis):
  '''Rotate array `X` `theta` degrees around axis `axis`'''
  c, s = np.cos(theta), np.sin(theta)
  if axis == 'x': return np.dot(X, np.array([
    [1.,  0,  0],
    [0 ,  c, -s],
    [0 ,  s,  c]
  ]))
  elif axis == 'y': return np.dot(X, np.array([
    [c,  0,  -s],
    [0,  1,   0],
    [s,  0,   c]
  ]))
  elif axis == 'z': return np.dot(X, np.array([
    [c, -s,  0 ],
    [s,  c,  0 ],
    [0,  0,  1.],
  ]))

def center(v):
  '''Center array `v` using dim with greatest variance as unit vector'''
  _min = np.min(v)
  _max = np.max(v)
  v = (v-_min) / (_max-_min) # centers 0:1
  v = (v-0.5)*2 # centers -1:1
  # 0 out the mean of each axis
  v[:,0] -= np.mean(v[:,0])
  v[:,1] -= np.mean(v[:,1])
  if np.shape(v)[1] > 2:
    v[:,2] -= np.mean(v[:,2])
  return v

def get_domain(v):
  '''Return the min,max of array `v`'''
  return [np.min(v), np.max(v)]

def get_model_json(animal_name):
  '''Process the data for an animal with `animal_name` in its filename'''
  files = [j for j in glob.glob('out/*.npy') if '50000' in j and animal_name in j]
  d2_files = [j for j in files if '2d' in j]
  d3_files = [j for j in files if '3d' in j]
  d2 = np.load(d2_files[0])
  d3 = np.load(d3_files[0])
  d2 = center(d2)
  d3 = center(d3)
  if rotations.get(animal_name, False):
    d3 = rotate(d3, rotations[animal_name], 'x')
  d2 = [[round(k, 4) for k in j] for j in d2.tolist()]
  d3 = [[round(k, 4) for k in j] for j in d3.tolist()]
  with open('json/' + animal_name + '.json', 'w') as out:
    json.dump({
      '2d': d2,
      '3d': d3,
    }, out)

# good animals
r = np.pi/2
rotations = {
  'armadillo_2': r,
  'bird_2': r,
  'bison': 0,
  'cockatiel': r,
  'cow': r,
  'crocodile_2': r,
  'dachshund': 0,
  'deer': 0,
  'lizard': 0,
  'seahorse_2': r,
  'snek_2': r,
  'tuna': 0,
  'turtle': r,
  'wolf': 0,
  'shark': 0,
}

if __name__ == '__main__':

  if not os.path.exists('json'):
    os.makedirs('jsons')

  for i in rotations:
    get_model_json(i)