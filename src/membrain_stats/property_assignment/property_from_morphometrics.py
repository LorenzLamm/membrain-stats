import os
from membrain_pick.dataloading.data_utils import load_mesh_from_hdf5, store_mesh_in_hdf5, get_csv_data
from sklearn.neighbors import NearestNeighbors
import numpy as np

def find_paired_morphometrics_file(h5_filename, morphometrics_folder):
    base_name = os.path.splitext(os.path.basename(h5_filename))[0]
    morphometrics_file = os.path.join(morphometrics_folder, f"{base_name}.csv")
    if os.path.exists(morphometrics_file):
        return morphometrics_file
    else:
        return None

def property_from_morphometrics(
    h5_folder: str,
    morphometrics_folder: str,
    out_folder: str,
    pixel_size_multiplier: float,
    max_distance_for_assignment: float = 50.0,
):
    """
    Assign properties to meshes based on morphometrics data.

    Parameters
    ----------
    h5_folder : str
        Path to the folder containing H5 files with mesh data.
    morphometrics_folder : str
        Path to the folder containing morphometrics data.
    out_folder : str
        Path to the folder where the output meshes with assigned properties will be stored.
    pixel_size_multiplier : float
        Multiplier to convert pixel size to physical units.

    Returns
    -------
    None
        The function saves the meshes with assigned properties to the specified output folder.
    """
    is_file = os.path.isfile(h5_folder)
    if is_file:
        h5_filenames = [h5_folder]
    else:
        h5_filenames = [os.path.join(h5_folder, f) for f in os.listdir(h5_folder) if f.endswith('.h5')]

    for filename in h5_filenames:
        if filename.endswith(".h5"):
            mesh_path = filename
            filename = os.path.basename(filename)
            if not os.path.isfile(morphometrics_folder):
                morphometrics_file = find_paired_morphometrics_file(filename, morphometrics_folder)
            else:
                morphometrics_file = morphometrics_folder
            if morphometrics_file is None:
                print(f"No paired morphometrics file found for {filename}. Skipping.")
                continue
            print(f"Processing {filename} with morphometrics from {morphometrics_file}")
            mesh = load_mesh_from_hdf5(mesh_path)
            morphometrics_data, header = get_csv_data(morphometrics_file, return_header=True, with_header=True)

            header = list(header)
            x_column = header.index('xyz_x')
            y_column = header.index('xyz_y')
            z_column = header.index('xyz_z')
            morphometrics_coords = morphometrics_data[:, [x_column, y_column, z_column]] * pixel_size_multiplier
            
            # compute nearest neighbor for all points in the mesh
            nbrs = NearestNeighbors(n_neighbors=1, algorithm='auto').fit(morphometrics_coords)
            distances, indices = nbrs.kneighbors(mesh['points'])
            distances, indices = distances.flatten(), indices.flatten()
            assignment_mask = distances <= max_distance_for_assignment

            min_distances = np.ones_like(distances) * 1e6
            print(f"Nearest neighbor assignment done. We found {np.sum(~assignment_mask)} points without close morphometrics (>{max_distance_for_assignment} Angstrom). These points will get nan values for all properties.")
            skip_columns = ['index', 'xyz_x', 'xyz_y', 'xyz_z', 'area']
            # assign properties to mesh points based on nearest neighbor
            for i, col in enumerate(header):
                if col in skip_columns:
                    continue  # skip columns
                    
                property_values = morphometrics_data[indices, i].flatten()
                if col.endswith('_dist'):
                    min_distances = np.minimum(min_distances, property_values)
                property_values[~assignment_mask] = np.nan  # assign nan to points without close morphometrics
                mesh[col] = property_values
                print(f"Assigned property '{col}' to mesh.")

            min_distances[~assignment_mask] = np.nan
            mesh['min_morphometrics_distance'] = min_distances


            out_path = os.path.join(out_folder, filename)
            os.makedirs(out_folder, exist_ok=True)
            store_mesh_in_hdf5(
                out_file=out_path,
                points=mesh['points'],
                faces=mesh['faces'],
                **{k: v for k, v in mesh.items() if k not in ['points', 'faces']}
            )
            print(f"Saved mesh with assigned properties to {out_path}")

