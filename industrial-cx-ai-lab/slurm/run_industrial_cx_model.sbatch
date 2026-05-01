#!/bin/bash
#SBATCH --job-name=industrial-cx-ai-lab
#SBATCH --output=artifacts/slurm-%j.out
#SBATCH --error=artifacts/slurm-%j.err
#SBATCH --time=00:05:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=2G

set -euo pipefail

cd "${SLURM_SUBMIT_DIR:-$(pwd)}"
python3 industrial-cx-ai-lab/src/run_pipeline.py
