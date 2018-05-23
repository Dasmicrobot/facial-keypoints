FROM continuumio/miniconda3

# Set the ENTRYPOINT to use bash
# (this is also where you’d set SHELL,
# if your version of docker supports this)
ENTRYPOINT ["/bin/bash", "-c"]

ADD app app/
ADD detector_architectures detector_architectures/

WORKDIR app

# Use the environment.yml to create the conda environment.
RUN [ "conda", "env", "create", "-f", "environment.yml" ]

EXPOSE 8080

CMD [ "source activate detector && gunicorn -w 4 -b 127.0.0.1:8080 app:app" ]