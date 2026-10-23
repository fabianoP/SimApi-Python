FROM python:3.12.12-slim-bookworm@sha256:593bd06efe90efa80dc4eee3948be7c0fde4134606dd40d8dd8dbcade98e669c

ARG ENERGYPLUS_TO_FMU_VERSION=3.1.0
ARG ENERGYPLUS_TO_FMU_SHA256=24eceb256367f57ddb79f64de9e59d8b3eeb731a30cfa154813dda8a97c53b51

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        ca-certificates \
        curl \
        unzip \
    && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home --home-dir /home/fmu --shell /bin/bash --uid 1000 fmu \
    && install -d -o fmu -g fmu /home/fmu/code/energy/test /home/fmu/code/fmu_location

WORKDIR /home/fmu/code

COPY requirements.txt .
RUN python -m pip install --no-cache-dir --requirement requirements.txt

RUN curl --fail --location --show-error \
        "https://github.com/lbl-srg/EnergyplusToFMU/releases/download/v${ENERGYPLUS_TO_FMU_VERSION}/EnergyPlusToFMU-v${ENERGYPLUS_TO_FMU_VERSION}.zip" \
        --output /tmp/energyplus-to-fmu.zip \
    && echo "${ENERGYPLUS_TO_FMU_SHA256}  /tmp/energyplus-to-fmu.zip" | sha256sum --check --strict \
    && unzip -q /tmp/energyplus-to-fmu.zip -d /home/fmu/code/energy \
    && rm /tmp/energyplus-to-fmu.zip \
    && cd /home/fmu/code/energy/Scripts/linux \
    && ./test-c-exe.sh \
    && chown -R fmu:fmu /home/fmu/code/energy

COPY --chown=fmu:fmu . .
COPY --chmod=755 run.sh /run.sh

USER fmu

EXPOSE 8000
CMD ["/run.sh"]
