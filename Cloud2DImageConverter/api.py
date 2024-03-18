# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/03_api.ipynb.

# %% auto 0
__all__ = ['run', 'color_matrix']

# %% ../nbs/03_api.ipynb 1
from . import spherical_projection as sp
from . import image_generator as ig
from . import data
from tqdm import tqdm
import numpy as np
import shutil
import os

# %% ../nbs/03_api.ipynb 2
def run(data_path, results_path, batch_size=500, fov_up=3.0, fov_down=-25.0, width=1024, height=64, is_label=True):
    velodyne_path = data_path+"velodyne"
    label_path = data_path + "labels" if is_label else None
    max_len = len(os.listdir(velodyne_path))
    if batch_size > max_len: 
        batch_size = max_len-1

    if os.path.exists(results_path): shutil.rmtree(results_path)
    os.makedirs(results_path)
    os.makedirs(results_path+"reflectance")
    os.makedirs(results_path+"depth")
    if is_label:
        os.makedirs(results_path+"segmentation_mask")

    for batch in tqdm(range(batch_size, max_len, batch_size), desc="Batch:"):
        start, end = ig.define_range(batch, batch_size, max_len)
        velodyne_list = sorted(os.listdir(velodyne_path))[start:end]
        label_list = sorted(os.listdir(label_path))[start:end] if is_label else None
        point_cloud = data.load_data(velodyne_path, velodyne_list, label_path, label_list)
        projection_dict = ig.do_projection(point_cloud, fov_up, fov_down, width, height, is_label)
        ig.create_images(projection_dict, results_path)

# %% ../nbs/03_api.ipynb 3
def color_matrix(matrix):
    matrix = np.vectorize(data.learning_map_inv.get)(matrix)
    colored_matrix =  np.empty(matrix.shape + (3,), dtype=np.uint8)
    color_map = data.color_map.items()
    for key, value in color_map:
        indices = np.where(matrix == key)
        colored_matrix[indices] = value
    matrix = colored_matrix
    return matrix
