In progress
================

## Conda environment

https://stackoverflow.com/a/41274348/906265

- Export conda environment:
`$ conda env export | grep -v "^prefix: " > conda_requirements.yml`

- Create environment:
`$ conda env create -f conda_requirements.yml`

- Activate environment:
`source activate face-app`

## Run app

`gunicorn -w 4 -b 0.0.0.0:5000 -k gevent app:app`


