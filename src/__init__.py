"""Cap native thread pools before numpy/torch/sklearn start them.

With 20 cores, sklearn's OpenMP, joblib (RF n_jobs) and torch's OpenMP pool otherwise
oversubscribe the CPU and can spin indefinitely (observed: RF fit hanging at ~1500% CPU).
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "8")
