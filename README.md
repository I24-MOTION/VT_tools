# VT-tools
### I-24 MOTION analytics code for speed field and virtual trajectory computation
#### Version: 1.0
#### Last updated: 2024-02-13

## Overview

VT-tools is an analytics toolbox for transforming large amounts of imperfect vehicle trajectory data into high-resolution spatiotemporal speed fields and generating virtual trajectories through these speed fields. Virtual trajectories have the advantage of being strongly based in empirical data, while containing no consistency imperfections and being generally smooth. These hypothetical trajectories can also be compared more readily, since they can be spawned at specific times and sampling rates.

## Use agreement

Use of this software is subject to the license (BSD 3-clause) included in the code repository. The following terms also apply to the I-24 MOTION project's data and software.

1. You are free to use this software and data in academic and commercial work. 
2. I-24 MOTION datasets contain anonymous trajectories. Any activities to re-identify individuals in the dataset or activities that may cause harm to individuals in the dataset are prohibited.
3. When you use I-24 MOTION software and/or data in published academic work, you are required to include the following relevant citations. This allows us to aggregate statistics on the data use in publications:

VT-tools and associated data:

> Ji, J., Wang, Y., Gloudemans, D., Zachár, G., Barbour, W., & Work, D. B. (2024, February). Virtual Trajectories for I–24 MOTION: Data and Tools. In 2024 Forum for Innovative Sustainable Transportation Systems (FISTS) (pp. 1-6). IEEE.

```
@inproceedings{ji2024virtual,
  title={Virtual Trajectories for I--24 MOTION: Data and Tools},
  author={Ji, Junyi and Wang, Yanbing and Gloudemans, Derek and Zach{\'a}r, Gergely and Barbour, William and Work, Daniel B},
  booktitle={2024 Forum for Innovative Sustainable Transportation Systems (FISTS)},
  pages={1--6},
  year={2024},
  organization={IEEE}
}
```

I24-MOTION System:

> Gloudemans, D., Wang, Y., Ji, J., Zachár, G., Barbour, W., Hall, E., Cebelak, M., Smith, L. and Work, D.B., 2023. I-24 MOTION: An instrument for freeway traffic science. Transportation Research Part C: Emerging Technologies, 155, p.104311.

```
@article{gloudemans202324,
  title={I-24 MOTION: An instrument for freeway traffic science},
  author={Gloudemans, Derek and Wang, Yanbing and Ji, Junyi and Zach{\'a}r, Gergely and Barbour, William and Hall, Eric and Cebelak, Meredith and Smith, Lee and Work, Daniel B},
  journal={Transportation Research Part C: Emerging Technologies},
  volume={155},
  pages={104311},
  year={2023},
  publisher={Elsevier}
}
```

4. You are free to create and share derivative products as long as you maintain the terms above. 
5. The data and software is provided “As is.” We make no other warranties, express or implied, and hereby disclaim all implied warranties, including any warranty of merchantability and warranty of fitness for a particular purpose.

## Requirements

VT-tools can be run as stand-alone code or imported as a library for part of your own analysis. The requirements for running the code are as follows:
- Python 3.10
- Supporting Python libraries: Pandas, Numpy, Matplotlib, ijson, tqdm, Jupyter-lab (optional, for opening Python notebooks)
- A `requirements.txt` file is provided for creating a new Python environment for VT-tools if you wish. This is the officially supported method for running VT-tools, since the code was validated on this exact set of dependency versions. The process for creating a new environment is below.


## Clean installation

Starting with a clean Python environment (i.e., through Conda or venv) with the correct Python version and dependencies is the officially supported method for running VT-tools. The instructions for doing so using the Anaconda Python distribution are as follows.

- Create a new environment with Python 3.10 (you can substitute "vt-tools" for your own name if you wish): `conda create -n vt-tools python=3.10`. 
- Activate the new environment (substitute "vt-tools for your own name if you altered it): `conda activate vt-tools`. 
- Change directory to the VT-tools location: `cd [PATH_TO_VT_TOOLS]`.
- Install Python library dependencies: `pip install -r requirements.txt`.
