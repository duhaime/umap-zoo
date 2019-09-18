from get_json import get_model_json
import vertices, umap, json, os
import numpy as np

min_dist = 0.0001
n_neighbors = 50
n_vertices = 50000

filename = 'trump-{}'.format(n_vertices)
v = vertices.ObjParser('../data/obj/trump.obj').get_n_vertices(n_vertices)
np.save(os.path.join('out', filename + '-3d'), v)
# project to 2D
o = umap.UMAP(min_dist=min_dist, n_neighbors=n_neighbors).fit_transform(v)
np.save(os.path.join('out', filename + '-2d'), o)
# save the model json for visualizing
get_model_json('trump')