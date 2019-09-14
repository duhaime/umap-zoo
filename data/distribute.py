# projects each animal down to 2d using various params

import matplotlib
matplotlib.use('agg')
import vertices, umap, glob, os, sys
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from random import randint
import numpy as np

for i in ['out', 'plots', 'json']:
  if not os.path.exists(i):
    os.makedirs(i)

worker_id = int(sys.argv[1])
n_verts_options = [50000, 100000, 500000]
min_dist_options = [0.0001]
n_neighbors_options = [200, 500, 1000]
models = glob.glob(os.path.join('obj', '*.obj'))

param_idx = 0
n_workers = len(n_verts_options) \
  * len(min_dist_options) \
  * len(n_neighbors_options) \
  * len(models)
print(' * workers required:', n_workers)

# distribute over n processes; n=number of objs in objs/*.obj
for n_verts in n_verts_options:
  for min_dist in min_dist_options:
    for n_neighbors in n_neighbors_options:
      for i in models:
        param_idx += 1
        if (param_idx%n_workers) != worker_id: continue
        if worker_id > n_workers: continue # too many workers requested
        filename = '{}-{}-{}-{}-{}-{}'.format(
          os.path.basename(i),
          axis,
          rotation,
          n_verts,
          min_dist,
          n_neighbors)
        print(' * processing', filename, 'with params', param_idx)
        # get the requested number of verts
        v = vertices.ObjParser(i).get_n_vertices(n_verts)
        np.save(os.path.join('out', filename + '-3d'), v)
        # project to 2D
        o = umap.UMAP(min_dist=min_dist, n_neighbors=n_neighbors).fit_transform(v)
        np.save(os.path.join('out', filename + '-2d'), o)
        # plot the result
        plt.clf()
        plt.scatter(o[:,0], o[:,1], s=0.01)
        plt.title(filename)
        plt.savefig(os.path.join('plots', filename + '.png'))
