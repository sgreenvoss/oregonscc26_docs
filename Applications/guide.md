### HPC Execution Checklist

- [ ] **1. Manage Terminal Session (`tmux`)**
  - Create a new session: `tmux new -s <SESSION_NAME>`
  - List existing sessions: `tmux ls`
  - Reattach to an existing session: `tmux attach -t <SESSION_NAME>`
- [ ] **2. Configure CPU & Memory Core-Binding (`numactl`)**
  - Check NUMA hardware layout: `numactl --hardware`
  - Bind CPU and matching memory location: `numactl --cpunodebind=<NODE_ID> --membind=<NODE_ID> <COMMAND>`
- [ ] **3. Set GPU Visibility**
  - Set active GPU(s): `export CUDA_VISIBLE_DEVICES=0` (or `0,1` for multiple GPUs, or `""` for no GPU)
- [ ] **4. Submit Tasks**
  - **Option A (Batch Job):** Create a Slurm job script (e.g., `job.sh`) and submit it via `sbatch job.sh`
  - **Option B (Direct Run):** Execute your command directly using the currently allocated resources
- [ ] **5. Reinstall Dependencies (Remote Session Reminder)**
  - Whenever you start a new remote session, re-activate your environment and reinstall all required dependencies and libraries before running your code
- [ ] **6. Monitor & Kill a Task**
  - Check active GPU / CPU processes: `nvtop` (GPU) or `htop` (CPU)
  - Terminate a process: `kill -9 <PID>` (or `scancel <JOB_ID>` for Slurm jobs)  *always double-check with teammates before killing shared processes*
