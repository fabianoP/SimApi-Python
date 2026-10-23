# EnergyPlus 9.0.1 is x86_64-only; Apple Silicon runs this image through Docker's amd64 emulation.
FROM --platform=linux/amd64 debian:bookworm-20241016-slim@sha256:d83056144b2dd301730d2739635c8cbdeaaae20d6887146434184f8c060f03ce

ARG MINIFORGE_VERSION=24.3.0-0
ARG MINIFORGE_SHA256=23367676b610de826f50f7ddc91139a816d4b59bd4c69cc9b6082d9b2e7fe8a3
ARG ENERGYPLUS_VERSION=9.0.1
ARG ENERGYPLUS_BUILD=bb7ca4f0da
ARG ENERGYPLUS_SHA256=5018f22c4ce230cadda7deef7ba796af6e3ed80380f7f486b2b3b8c61fc311d9

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    CONDA_DIR=/opt/conda \
    CONDA_ENV=/opt/conda/envs/simapi \
    ENERGYPLUS_DIR=/opt/EnergyPlus-9-0-1

RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates curl bzip2 libgomp1 \
    && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL --retry 3 \
        "https://github.com/conda-forge/miniforge/releases/download/${MINIFORGE_VERSION}/Miniforge3-${MINIFORGE_VERSION}-Linux-x86_64.sh" \
        -o /tmp/miniforge.sh \
    && echo "${MINIFORGE_SHA256}  /tmp/miniforge.sh" | sha256sum -c - \
    && bash /tmp/miniforge.sh -b -p "${CONDA_DIR}" \
    && rm /tmp/miniforge.sh

COPY conda_requirements.txt requirements.txt /tmp/
RUN "${CONDA_DIR}/bin/conda" config --system --set channel_priority strict \
    && "${CONDA_DIR}/bin/conda" create --yes --name simapi --file /tmp/conda_requirements.txt \
    && "${CONDA_ENV}/bin/python" -m pip install --no-cache-dir --requirement /tmp/requirements.txt \
    && "${CONDA_DIR}/bin/conda" clean --all --yes \
    && rm /tmp/conda_requirements.txt /tmp/requirements.txt

RUN curl -fsSL --retry 3 \
        "https://github.com/NREL/EnergyPlus/releases/download/v${ENERGYPLUS_VERSION}/EnergyPlus-${ENERGYPLUS_VERSION}-${ENERGYPLUS_BUILD}-Linux-x86_64.tar.gz" \
        -o /tmp/energyplus.tar.gz \
    && echo "${ENERGYPLUS_SHA256}  /tmp/energyplus.tar.gz" | sha256sum -c - \
    && mkdir /tmp/energyplus \
    && tar -xzf /tmp/energyplus.tar.gz -C /tmp/energyplus \
    && mv "/tmp/energyplus/EnergyPlus-${ENERGYPLUS_VERSION}-${ENERGYPLUS_BUILD}-Linux-x86_64/EnergyPlus-9-0-1" "${ENERGYPLUS_DIR}" \
    && rm -rf /tmp/energyplus /tmp/energyplus.tar.gz

RUN useradd --create-home --uid 1000 --shell /bin/bash deb \
    && mkdir -p /home/deb/code/volume /home/deb/code/fmu_location /home/deb/code/store_incoming_json \
    && chown -R deb:deb /home/deb

ENV PATH="${CONDA_ENV}/bin:${ENERGYPLUS_DIR}:${PATH}"

WORKDIR /home/deb/code
COPY --chown=deb:deb . /home/deb/code/
RUN cp /home/deb/code/run.sh /run.sh \
    && chmod +x /run.sh

USER deb

CMD ["/run.sh"]
