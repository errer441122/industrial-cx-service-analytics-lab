#!/usr/bin/env bash
#SBATCH --job-name=industrial_service_scoring
#SBATCH --array=0-9
#SBATCH --time=00:10:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=2G
#SBATCH --partition=cpu

set -euo pipefail

# HPC-ready packaging only. Not executed on a real cluster, partner,
# employer, or production scheduler.

cd "${SLURM_SUBMIT_DIR:-$PWD}"

python industrial-cx-ai-lab/src/run_pipeline.py --partition "${SLURM_ARRAY_TASK_ID:-0}"
