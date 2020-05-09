FROM {{ cookiecutter.docker_image }}

ENV PYTHONDONTWRITEBYTECODE=true
ARG WORKSPACE=/workspace
ARG PROJECT_DIR=${WORKSPACE}/{{ cookiecutter.project_slug }}
WORKDIR ${WORKSPACE}
COPY scripts ${WORKSPACE}/scripts
COPY environment.yaml ${PROJECT_DIR}/environment.yaml
COPY setup.cfg ${PROJECT_DIR}/setup.cfg
COPY setup.py ${PROJECT_DIR}/setup.py
COPY src ${PROJECT_DIR}/src

RUN apt-get update --fix-missing &&\
    DEBIAN_FRONTEND=noninteractive apt-get install -y wget ca-certificates git bzip2 &&\
    rm -rf /var/lib/apt/lists/* &&\
    wget --quiet https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    /opt/conda/bin/conda init bash


#Add this line to load dependencies from an environment file  /opt/conda/bin/conda env update -n base conda --file ${PROJECT_DIR}/environment.yaml
# Else be sure to add the dependencies of your project
RUN /opt/conda/bin/conda run -n base pip install -e ${PROJECT_DIR} &&\
    /opt/conda/bin/conda clean -afy &&\
    find /opt/conda/ -follow -type f -name '*.a' -delete &&\
    find /opt/conda/ -follow -type f -name '*.pyc' -delete &&\
    find /opt/conda/ -follow -type f -name '*.js.map' -delete
