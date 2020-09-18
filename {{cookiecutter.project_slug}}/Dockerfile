FROM python:{{ cookiecutter.pyver }}-slim

ENV PYTHONDONTWRITEBYTECODE=true
ARG WORKSPACE=/workspace
ARG PROJECT_DIR=${WORKSPACE}/{{ cookiecutter.project_slug }}
WORKDIR ${WORKSPACE}
COPY scripts ${WORKSPACE}/scripts
COPY setup.cfg ${PROJECT_DIR}/setup.cfg
COPY setup.py ${PROJECT_DIR}/setup.py
COPY src ${PROJECT_DIR}/src
COPY requirements ${PROJECT_DIR}/requirements

RUN apt-get update --fix-missing \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y wget ca-certificates git bzip2 \
    && rm -rf /var/lib/apt/lists/* \
    && pip install pip-tools

WORKDIR ${PROJECT_DIR}
RUN pip-compile ${PROJECT_DIR}/reqs.in --output-file ${PROJECT_DIR}/reqs.txt \
    && pip-compile ${PROJECT_DIR}/tests.in --output-file ${PROJECT_DIR}/tests.txt \
    && pip install '.[tests]'
    && pip-sync ${PROJECT_DIR}/reqs.txt ${PROJECT_DIR}/tests.txt
