# HPC / Slurm Review Shortcut

This folder makes HPC evidence visible from the repository root.

The project does not claim real CINECA, IT4LIA, BI-REX, or Ducati cluster execution. It shows how the workload would be packaged for a Linux/Slurm environment and points to runnable local equivalents.

## Files

- `run_pipeline.sbatch` - top-level Slurm entrypoint for the reviewer.
- `industrial-cx-ai-lab/slurm/run_industrial_cx_model.sbatch` - lab-specific Slurm script.
- `production-sim-stack/slurm/run_iot_scoring_array.sbatch` - job-array style production simulation.

## Local Equivalent

```bash
python3 industrial-cx-ai-lab/src/run_pipeline.py
python3 production-sim-stack/src/orchestrate.py
python3 production-sim-stack/src/mqtt_simulator.py
```
