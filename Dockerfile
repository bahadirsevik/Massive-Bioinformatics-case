# Dockerfile for Reproducible Bioinformatics Pipeline
FROM mambaorg/micromamba:1.5.1

# We need root temporarily to fix any timezone or core utilities
USER root
RUN apt-get update && apt-get install -y procps && rm -rf /var/lib/apt/lists/*
USER $MAMBA_USER

# Copy our environment dependencies and install them in the base micromamba environment
COPY --chown=$MAMBA_USER:$MAMBA_USER environment.yml /tmp/env.yml
RUN micromamba install -y -n base -f /tmp/env.yml && \
    micromamba clean --all --yes

# Set the working directory
WORKDIR /app

# Copy the rest of the project files to the container
COPY --chown=$MAMBA_USER:$MAMBA_USER . /app

# The micromamba entrypoint handles initializing the conda environment
# We pass snakemake as the default execution command
ENTRYPOINT ["/usr/local/bin/_entrypoint.sh", "snakemake", "--cores", "1"]
