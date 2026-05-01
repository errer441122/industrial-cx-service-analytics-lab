#!/bin/bash
#SBATCH --job-name=industrial-cx-review
#SBATCH --output=logs/industrial-cx-review-%j.out
#SBATCH --error=logs/industrial-cx-review-%j.err
#SBATCH --time=00:20:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --partition=cpu

set -euo pipefail

cd "${SLURM_SUBMIT_DIR:-$PWD}"

if [ -f ".venv/bin/activate" ]; then
  source ".venv/bin/activate"
fi

python3 industrial-cx-ai-lab/src/run_pipeline.py
python3 production-sim-stack/src/orchestrate.py
python3 production-sim-stack/src/mqtt_simulator.py
python3 ml-baseline/train_model.py
