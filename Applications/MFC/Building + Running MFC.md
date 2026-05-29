In an interactive session on ORCA, I ran:
- git clone (the mfc code)
- cd MFC
- module load gcc
- module load mpich
- module load python
- ./mfc.sh build --gpu
	- you should do this with -j 4 or 8 or something but i decided to just build serially

This could have gone in the short partition but i put in normal just in case
```
#!/usr/bin/env bash

#SBATCH --job-name=mfc-test
#SBATCH --partition=normal      
#SBATCH --time=02:00:00        
#SBATCH --ntasks=8           
#SBATCH --error=riemann/mfc-test.err.txt 
#SBATCH --output=riemann/mfc-test.out.txt
  

module load gcc
module load mpich
module load python

  
cd /home/sgreenvoss/mfc/MFC
./mfc.sh run examples/2D_riemann_test/case.py -n 8
```
Above went pretty slow (16ish mins), should try again with more tasks, more cores, maybe even a GPU (woag)

Aside: using htop doesn't reveal the processes, only the core utilization. Is viewing processes disabled on ORCA?

To view the output as a video, run ./mfc.sh viz examples/2D_riemann_test/ --var pres --step all --mp4
- the [example page](https://mflowcode.github.io/documentation/examples.html#:~:text=errors.csv.-,2D%20Riemann%20Test%20(2D),-Reference%3A) talks about density but selecting --var dens didn't do anything, so I used pressure for this example. 

To view the video, scp to your local computer:
- scp sgreenvoss@login.orca.pdx.edu:/home/sgreenvoss/mfc/MFC/examples/2D_riemann_test/viz/pres.mp4 output

Next, I increased ntasks to 16: 
```
#!/usr/bin/env bash
#SBATCH --job-name=mfc-test
#SBATCH --partition=short      
#SBATCH --time=02:00:00        
#SBATCH --ntasks=16           
#SBATCH --error=riemann/16_mfc-test.err.txt 
#SBATCH --output=riemann/16_mfc-test.out.txt

module load gcc
module load mpich
module load python

cd /home/sgreenvoss/mfc/MFC
./mfc.sh run examples/2D_riemann_test/case.py -n 16
```
This is still running on only one node, because ntasks != nodes

Total time for 8 tasks: 691s
Total time for 16 tasks: 368s


The docs tell you to use their [batch mode](https://mflowcode.github.io/documentation/running.html#:~:text=can%20be%20appended.-,Batch%20Execution,-The%20MFC%20detects) for running on clusters, but may need to create our own template for the different cluster


Don't run two jobs at once on the same case, they will step on each others' toes!


I then started running their performance test with different numbers of processors:

```
./mfc.sh run -n 64 -j $(nproc) examples/3D_performance_test/case.py \
        -t pre_process simulation --case-optimization
```


| usage    | pre-process time | perf (lower is better) | time |
| -------- | ---------------- | ---------------------- | ---- |
| 32 cores | 3.56 s           | 3.93                   | 40 s |
| 64 cores | 5.35 s           | 2.78                   | 51 s |
I'm struggling to get it to run on the gpu because it needs non-gnu compilers. And then after it failing with that, it started failing on non-gpu tasks, so I cleaned and rebuilt.
