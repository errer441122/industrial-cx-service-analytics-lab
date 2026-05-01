# HPC / Slurm Review Shortcut

This folder makes HPC evidence visible from the repository root.

The project does not claim real CINECA, IT4LIA, BI-REX, IPAZIA, Ducati, or other cluster execution. It shows how the workload would be packaged for a Linux/Slurm environment and points to runnable local CPU equivalents.

## Files

| File | Purpose | Execution status |
| --- | --- | --- |
| `run_pipeline.sbatch` | Legacy top-level Slurm entrypoint for reviewer orientation. | Packaging only. |
| `run_industrial_scoring_array.sbatch` | Slurm job-array packaging for the industrial scoring pipeline. | Not submitted to a real cluster. |
| `industrial-cx-ai-lab/slurm/run_industrial_cx_model.sbatch` | Lab-specific batch script. | Packaging only. |
| `production-sim-stack/slurm/run_iot_scoring_array.sbatch` | Production simulation job-array sketch. | Packaging only. |

## Local Equivalent

```bash
python industrial-cx-ai-lab/src/run_pipeline.py
python production-sim-stack/src/orchestrate.py
python production-sim-stack/src/mqtt_simulator.py --dry-run --messages 5
python benchmarks/industrial_scoring_benchmark.py --quick
```

The benchmark writes `benchmarks/artifacts/local_cpu_benchmark.json` and is explicitly local CPU only.
