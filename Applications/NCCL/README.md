# Set up the test
- Step 1: Download NCCL https://github.com/NVIDIA/nccl -> $ make src.build CUDA_HOME=<path to cuda install>
- Step 2: Download NCCL-test https://github.com/NVIDIA/nccl-tests -> $ make -j CUDA_HOME=/path/to/cuda NCCL_HOME=/path/to/nccl (adding the path to the NCCL's build folder) 

# Topology
nvidia-smi topo -m

<img width="630" height="353" alt="image" src="https://github.com/user-attachments/assets/7e381cb7-4d4e-48c2-ad2a-c72cc4823cc9" />

nvidia-smi nvlink --status

<img width="494" height="368" alt="image" src="https://github.com/user-attachments/assets/5f6a7046-f48d-4c45-884e-6ab30e098d93" />


# Here is the result for 4 given examples
- Example A: CUDA_VISIBLE_DEVICES=0,1 \ ./build/all_reduce_perf -b 8 -e 1G -f 2 -g 2 -n 50 -w 10 -c 0
  
<img width="1529" height="693" alt="image" src="https://github.com/user-attachments/assets/b1178f19-0148-4cd8-aca1-99df694b1b97" />

- Example B: CUDA_VISIBLE_DEVICES=0,1 \ NCCL_DEBUG=WARN \ ./build/broadcast_perf -b 8 -e 32K -f 2 -g 2 -n 1000 -w 200 -c 0
  
<img width="1618" height="589" alt="image" src="https://github.com/user-attachments/assets/cd196132-3b2d-46b0-9cc7-200cffc77493" />

- Example C:

   mpirun -np 2 --bind-to numa \
  -x CUDA_VISIBLE_DEVICES=0,1 \
  -x NCCL_DEBUG=WARN \
  ./build/all_reduce_perf -b 8 -e 1G -f 2 -g 1 -n 50 -w 10 -c 0
  
  <img width="1037" height="1389" alt="image" src="https://github.com/user-attachments/assets/9cc1f01e-463e-4113-8196-a56843dd73d8" />

- Example D:
  
 #!/usr/bin/env bash \
set -euo pipefail \
PAIR="${PAIR:-0,1}" \
OUT="nccl_nvlink_$(date +%Y%m%d_%H%M%S)" \
mkdir -p "$OUT" \
nvidia-smi topo -m > "$OUT/topology.txt" \
nvidia-smi nvlink --status > "$OUT/nvlink_status.txt" \
nvidia-smi --query-gpu=index,name,clocks.max.sm --format=csv \
  > "$OUT/gpus.csv"
for COLL in all_reduce all_gather reduce_scatter broadcast; do
  CUDA_VISIBLE_DEVICES="$PAIR" NCCL_DEBUG=INFO NCCL_DEBUG_SUBSYS=INIT,GRAPH \
    ./build/${COLL}_perf -b 8 -e 1G -f 2 -g 2 -n 100 -w 20 -c 1 \
    > "$OUT/${COLL}.log" 2>&1
  echo "${COLL}: $(grep 'Avg bus bandwidth' "$OUT/${COLL}.log")"
done

<img width="1013" height="481" alt="image" src="https://github.com/user-attachments/assets/03a7fe8b-6dd9-472e-b729-73ab39bef0f1" />


# Report Format

<img width="601" height="310" alt="image" src="https://github.com/user-attachments/assets/e60ca01e-27ed-438c-8d9f-776adbe44fab" />

Required Content for the report

## 1. Identification 
   
- Team name, or individual names 
  
- Team affiliation
  
- Which benchmark or benchmarks your report covers 
  
## 2. Environment Details

- System specifications and configuration
  
- Instance type and node count used for the run
  
- OS and kernel version 
  
- Compiler selection and version 
  
- Every library the benchmark depends on, with its version and where it came from \
  
## 3. Binary and Tuning Information \

- Source of binary (self-compiled vs. vendor-provided) 
  
- Build scripts, and any modifications you made to the source
  
- The complete input or configuration file used for the run
  
- Optimization techniques applied 
  
- Performance tuning parameters, including any environment variables you set and why
- 
## 4. Results
  
- The complete, unedited final output. Do not paste a summary line on its own.
- 
How many times you ran the benchmark, and the spread across those runs. A
single run is a data point, not a result.

- A plot, where the benchmark produces a curve rather than one number
  
## 5. Performance Analysis 
  
- Your measured result stated as a percentage of theoretical peak
  
- An explanation of the gap between the two, whatever its size
  
- Identify potential bottlenecks
  
- Suggest areas for further investigation
  
- Recommend performance improvement strategies
## 6. NCCL
<img width="871" height="669" alt="image" src="https://github.com/user-attachments/assets/28fcb042-d785-40a3-9078-3899d2e07a1c" />

### Optimizing resources:
H100 arch: https://developer.nvidia.com/blog/nvidia-hopper-architecture-in-depth/

NCCL env variables: https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/env.html

NCCL operation doc: https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/collectives.html

NCCL code: https://github.com/NVIDIA/nccl

Github repo about optimizing, Technical blog? I'm sure this problem isn't new so there probably exists a technical blog about this
