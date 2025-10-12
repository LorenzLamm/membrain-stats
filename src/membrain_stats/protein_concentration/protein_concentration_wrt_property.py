from typing import List
import os
import numpy as np
import pandas as pd
import starfile
import trimesh
from sklearn.neighbors import NearestNeighbors
from matplotlib import pyplot as plt
from membrain_stats.utils.io_utils import (
    get_mesh_filenames,
    get_mesh_from_file,
)
from membrain_stats.membrane_edges.edge_from_curvature import (
    exclude_edges_from_mesh,
)
from membrain_stats.utils.wrt_utils import get_wrt_property_inputs


def reassign_properties_based_on_nearest_neighbors(
        orig_mesh: dict,
        mesh: dict,
) -> dict:

    nbrs = NearestNeighbors(n_neighbors=1, algorithm='auto').fit(orig_mesh['verts'])
    distances, indices = nbrs.kneighbors(mesh['verts'])
    distances, indices = distances.flatten(), indices.flatten()
    for key in orig_mesh.keys():
        if key in ['points', 'faces', 'labels', 'pixel_size', 'tomo_file']:
            continue
        # check whether the original mesh property is a numpy array and if yes has the same length as the number of vertices
        if not isinstance(orig_mesh[key], np.ndarray):
            print(f"Skipping property {key} as it is not a numpy array.")
            continue
        if len(orig_mesh[key]) != len(orig_mesh['verts']):
            print(f"Skipping property {key} as it has length {len(orig_mesh[key])} which is different from the number of vertices {len(orig_mesh['verts'])}.")
            continue
        print(f"Reassigning property {key}")
        mesh[key] = orig_mesh[key][indices]
    return mesh

def protein_concentration_wrt_property_folder(
    in_folder: str,
    out_folder: str,
    exclude_edges: bool = False,
    edge_exclusion_width: float = 50.0,
    pixel_size_multiplier: float = None,
    only_one_side: bool = False,
    with_respect_to_property: str = "scores",
    num_bins: int = 25,
):

    filenames = get_mesh_filenames(in_folder)
    mesh_dicts = [
        get_mesh_from_file(filename, pixel_size_multiplier=pixel_size_multiplier)
        for filename in filenames
    ]
    if exclude_edges:
        orig_mesh_dicts = mesh_dicts.copy()
        mesh_dicts = [
            exclude_edges_from_mesh(
                out_folder=out_folder,
                filename=filename,
                mesh_dict=mesh_dict,
                edge_exclusion_width=edge_exclusion_width,
            )
            for filename, mesh_dict in zip(filenames, mesh_dicts)
        ]
        mesh_dicts = [
            reassign_properties_based_on_nearest_neighbors(
                orig_mesh=orig_mesh,
                mesh=mesh,
            )
            for orig_mesh, mesh in zip(orig_mesh_dicts, mesh_dicts)
        ]

    meshes = [
        trimesh.Trimesh(
            vertices=mesh_dict["verts"],
            faces=mesh_dict["faces"],
        )
        for mesh_dict in mesh_dicts
    ]

    property_per_point, mesh_barycentric_areas, mesh_properties = (
        get_wrt_property_inputs(
            mesh_dicts=mesh_dicts,
            meshes=meshes,
            with_respect_to_property=with_respect_to_property,
        )
    )
    mesh_barycentric_areas /= 100  # convert to nm^2
    if only_one_side:
        mesh_barycentric_areas /= 2

    min_property, max_property = np.nanmin(mesh_properties), np.nanmax(mesh_properties)
    print(f"Property {with_respect_to_property} ranges from {min_property} to {max_property}")

    bins = np.linspace(min_property, max_property, num_bins)
    hist = np.histogram(property_per_point, bins=bins)[0]
    y_data = []
    for num_bin, protein_numbers in enumerate(hist):
        bin_lower = bins[num_bin]
        bin_upper = bins[num_bin + 1]
        area_mask = (mesh_properties >= bin_lower) & (mesh_properties < bin_upper)
        print(f"Bin {num_bin}: {bin_lower} - {bin_upper}, area: {np.sum(mesh_barycentric_areas[area_mask])} nm^2, proteins: {protein_numbers}")
        y_data.append(protein_numbers / np.sum(mesh_barycentric_areas[area_mask]))
    

    plt.figure()
    plt.plot(bins[:-1], y_data)
    plt.xlabel("Property")
    plt.ylabel("Area covered")
    plt.savefig("./protein_concentration_wrt_property.png")

    out_data = {
        "bin_lower": bins[:-1],
        "bin_upper": bins[1:],
        "concentration": y_data,
    }
    out_data = pd.DataFrame(out_data)
    starfile.write(
        out_data,
        os.path.join(out_folder, "protein_concentration_wrt.star"),
        float_format="%.12f",
    )
