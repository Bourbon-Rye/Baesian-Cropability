# Baesian-Cropability

The project focuses on air quality relation to food crops productivity using different statistical analysis and machine learning.

## Environment

To set up the `baesians` environment, tweak first the bundled `environment.yml` file and replace the `prefix` parameter with the path to your conda or miniconda installation. I.e. replace `C:\Users\YSHebron\anaconda3\envs\baesians` with possibly `C:\Users\<username>\anaconda3\envs\baesians` if you're on Windows and using Anaconda, or `/home/<username>/miniconda3/envs/scl` if you're on Linux and using Miniconda.

Then, create an environment using the bundled `environment.yml` file:

```sh
conda env create -f environment.yml
```

Activate the new environment using `conda activate baesians`. Verify that the environment was installed correctly using `conda env list`.
