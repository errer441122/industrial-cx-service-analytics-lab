#!/bin/bash
#SBATCH --job-name=industrial-iot-scoring
#SBATCH --output=artifacts/slurm-%A_%a.out
#SBATCH --error=artifacts/slurm-%A_%a.err
#SBATCH --array=0-3
#SBATCH --time=00:10:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=2G

set -euo pipefail

cd "${SLURM_SUBMIT_DIR:-$(pwd)}"
python3 production-sim-stack/src/orchestrate.py
