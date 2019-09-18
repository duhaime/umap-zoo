from get_json import get_model_json
import vertices, umap, json

filename = 'hotdog'
min_dist = 0.0001
n_neighbors = 50

v = vertices.ObjParser('../data/obj/hotdog.obj').get_n_vertices(50000)
np.save(os.path.join('out', filename + '-3d'), v)
# project to 2D
o = umap.UMAP(min_dist=min_dist, n_neighbors=n_neighbors).fit_transform(v)
np.save(os.path.join('out', filename + '-2d'), o)

get_model_json('hotdog')
