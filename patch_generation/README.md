## Adversarial Patch Generation for YOLOv5

This repository provides code to generate adversarial patches targeting YOLOv5.  
The generated patch can be **disguised inside any image of your choice** and optimized to fool the model into predicting a desired target class.

---

## Setup

You can either use the provided Conda environment or install the required dependencies manually.  
Make sure to install our customized fork of the [Adversarial Robustness Toolbox (ART)](https://github.com/Trusted-AI/adversarial-robustness-toolbox):

```shell
conda env create -f environment.yaml
conda activate dydec

cd adversarial-robustness-toolbox
pip install .
```

## Patch Generation

To reproduce our results, you can keep the default configuration in `patch_config.yaml`.
Otherwise, feel free to modify it according to your needs.

Run the following command to generate a patch:

```Shell
python generate_patch.py -mode single -load false
```

Set `-load true` if you already have a saved `.pkl` file and only want to run evaluation without regenerating the patch.

## Available Modes

You can control the patch-generation behavior using the `-mode` argument:

#### `single`

Generates a single adversarial patch — this is the mode used in our paper.

#### `collusion`

Generates a patch using **two pedestrians at the same time**.
This is **not** the same collusion setup described in the paper:

 - **Paper version:** a single generated patch is manually split into two.

 - **Code version:** the system places the disguised image on two pedestrians simultaneously during optimization.

For this mode, we typically use images containing two objects, e.g., `camellia_split.jpg` in the `disguises/` folder.

> **To faithfully replicate the collusion experiment from our paper:**<br>
> Generate a **single** patch, manually split it, and then apply each half to the pedestrians’ t-shirts

## Results

Generated patches are saved under:

`plots/patches/`

During training, additional artifacts such as loss curves, CCDF plots, and other diagnostics are stored in:

`plots/`

Validation outputs are written to:

`validation_results/`

If you run validation again, visualizations of all validated images (with the adversarial patch applied) appear in:

`plots/validation/`

These correspond to the results shown in **Figure 4** of our paper.

---

**P.S.**<br>
All currently existing files in the `results/` and `plots/` folders correspond to the outputs produced for our paper.
