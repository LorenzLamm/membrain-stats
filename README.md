# MemBrain-Stats

Membrain-Stats<sup>1</sup> is a Python project developed by the [CellArchLab](https://www.cellarchlab.com/) for computing membrane protein statistics in 3D for cryo-electron tomography (cryo-ET). 
It is part of the larger MemBrain package, which also includes MemBrain-pick for membrane protein detection and MemBrain-seg for membrane segmentation. The full MemBrain package can be found [here](https://github.com/CellArchLab/MemBrain-v2).

The goal of the package is to provide easy-to-use tools to analyze the distribution of membrane proteins in relation to the underlying membrane geometry. To this end, we provide the following functionalities:
- Protein concentration computation
- Protein concentration with respect to another point class (e.g., membrane edge)
- Protein concentration with respect to a membrane property (e.g., morphometrics property)
- (Geodesic) Nearest Neighbor distances (and orientations of neighbors to each other)
- (Geodesic) Nearest Neighbor distances with respect to another point class (e.g., membrane edge)
- (Geodesic) Ripley's statistics


<p align="center" width="90%">
    <img width="100%" src="https://github.com/user-attachments/assets/7cf780b8-c4ed-442c-84bb-e8afe0161cb6">
</p>


## Publication: 
Membrain-stats's functionalities are described in more detail in our [preprint](https://www.biorxiv.org/content/10.1101/2024.01.05.574336v2) [1].

```
[1] Lamm, L., Zufferey, S., Righetto, R.D., Wietrzynski, W., Yamauchi, K.A., Burt, A., Liu, Y., Zhang, H., Martinez-Sanchez, A., Ziegler, S., Isensee, F., Schnabel, J.A., Engel, B.D., and Peng, T, 2024. MemBrain v2: an end-to-end tool for the analysis of membranes in cryo-electron tomography. bioRxiv, https://doi.org/10.1101/2024.01.05.574336
```

## Usage:
For more details about how to use MemBrain-stats, refer to our [User Instructions](instructions_overview.md) document.

## Example Notebooks:

<p align="center" width="70%">
    <img width="100%" src="https://github.com/user-attachments/assets/0a20a67f-868e-400c-b100-eed32f63659a">
</p>

We provide an example jupyter notebook highlighting what can be done with MemBrain-stats [here](./examples/NN_orientation_ribosomes_example.ipynb). This is a very advanced example, using outputs from template matching and analyzing ribosome chains (this example was also shown in our preprint).

An example notebook (Colab tutorial) showcasing the pure functionalities of MemBrain-stats can be found here ([![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/CellArchLab/membrain_tutorial_scripts/blob/main/MemBrain_pick_example.ipynb)). Its workflow shows the generation of particle position predictions via MemBrain-pick, followed by analysis using MemBrain-stats.