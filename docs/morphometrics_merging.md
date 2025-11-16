# Compatibility with Surface Morphometrics Pipeline

MemBrain-stats can compute several simple membrane statistics. To enable the analysis of particle distributions with respect to also more advanced membrane properties, we make it possible to load outputs from the Surface Morphometrics Pipeline [1] into the membrane containers produced by MemBrain-pick.
This enables the joint analysis of particle positions with respect to different properties computed by the pipeline, like curvature or inter-membrane distance.

```
[1] Barad, Benjamin A., et al. "Quantifying organellar ultrastructure in cryo-electron tomography using a surface morphometrics pipeline." Journal of Cell Biology 222.4 (2023): e202204093.
```

## Morphometrics computation

To compute membrane morphometrics, please follow the instructions provided on the repository:
https://github.com/GrotjahnLab/surface_morphometrics

**Note**: It is important that you keep track of the membrane file naming and make sure that you can 1:1 match the outputs of MemBrain-pick with the outputs of the morphometrics (e.g., MemBrain-pick Tomo1_M5.h5 container corresponds to Morphometrics output Tomo1_M5.csv)

## Morphometrics merging into containers
Once you have MemBrain-pick predictions (for getting there, take a look at the [MemBrain-pick docs](https://github.com/CellArchLab/membrain-pick/blob/master/docs/Index.md)), and ran the Surface Morphometrics Pipeline on the same membranes, you can merge the morphometrics outputs into the MemBrain-pick containers using:

```
membrain_stats property_from_morphometrics --h5-path <path-to-membrainpick-output> --morphometrics-path <path-to-morphometrics-output>
```

Here is a more detailed overview of the different arguments:
### More options

- **`--h5-path`** (TEXT, required)  
  Path to the MemBrain-pick output container. Can also be a directory, in this case names of containers and morphometrics csvs have to match exactly (e.g. Tomo1_M5.h5 vs Tomo1_M5.csv)  
- **`--morphometrics-path`** (TEXT, required)  
  Path to the single `.csv` file containing the Surface Morphometrics outputs. Can also be a directory, in this case names of containers and morphometrics csvs have to match exactly (e.g. Tomo1_M5.h5 vs Tomo1_M5.csv)  
- **`--out-folder`** (TEXT)  
  Path to the folder where the augmented `.h5` files (with morphometrics added) will be stored.  
  **Default:** `./stats/predictions_with_morphometrics`
- **`--pixel-size-multiplier`** (FLOAT)  
  Scaling factor applied to morphometrics coordinates to match MemBrain-pick coordinates.  
  Only needed if the two pipelines use different pixel-size conventions.  
  **Default:** `1.0`
- **`--max-distance-for-assignment`** (FLOAT)  
  Maximum allowed distance (in Ångström) between a membrane vertex and its nearest morphometrics point.  
  If the nearest point is farther than this cutoff, the vertex receives `nan` values.  
  **Default:** `50.0`
- **`--help`**  
  Show this message and exit.


### Example
```bash
membrain_stats property_from_morphometrics \
  --h5-path ./stats/predictions/ \
  --morphometrics-path ./morphometrics/ \
  --out-folder ./stats/predictions_with_morphometrics/ \
  --pixel-size-multiplier 1.0 \
  --max-distance-for-assignment 50.0
```

## Further analysis
Once the morphometrics have been merged into the MemBrain-pick containers, you can use the `membrain_stats protein_concentration_wrt_property` functionality to analyze particle distributions with respect to the different morphometrics properties.
Find more information about this functionality [here](protein_concentrations.md#protein-concentration-with-respect-to-morphometrics-property).