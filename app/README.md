Face detector using webcam
================

## Setup Conda environment

https://stackoverflow.com/a/41274348/906265

- Export conda environment:
`$ conda env export | grep -v "^prefix: " > conda_requirements.yml`

- Create environment:
`$ conda env create -f conda_requirements.yml`

- Activate environment:
`source activate faceapp`

## Run app

`python api.py`


