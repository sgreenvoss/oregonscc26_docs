Notes taken while working on the STREAM benchmark
## how is memory bandwidth calculated by STREAM
**Memory bandwidth**
The **Stream convention**: sums the amount of data that the application code explicitly reads plus the amount of data that the application code explicitly writes.[[1]](https://en.wikipedia.org/wiki/Memory_bandwidth#cite_note-1) Using the previous 1 million byte copy example, the STREAM bandwidth would be counted as 1 million bytes read plus 1 million bytes written in one second, for a total of 2 million bytes per second. The STREAM convention is most directly tied to the user code, but may not count all the data traffic that the hardware is actually required to perform.

## Intel: how to compute max memory bandwidth
https://www.intel.com/content/www/us/en/support/articles/000056722.html

## Our numbers: 
https://www.intel.com/content/www/us/en/products/sku/237564/intel-xeon-gold-6548y-processor-60m-cache-2-50-ghz/specifications.html
max memory frequency: DDR5 5200 MT/s
max number of channels: 8
"bytes of width?" bus width maybe: 8

5200 x 8 x 8 = 332,800 MB/s -> 332.8 GB/s
confirmed by this specs page: https://www.techpowerup.com/cpu-specs/xeon-gold-6548y.c3420
TWO SOCKETS, so peak is ~664 GB/s

## Compiling STREAM
Installed intel compilers, to use: `source /opt/intel/oneapi/setvars.sh intel64`

#### Intel's recommended settings

`icx stream.c -o stream_c.exe -DNTIMES=100 -DOFFSET=0 -DSTREAM_TYPE=double -DSTREAM_ARRAY_SIZE=268435456 -Wall -mcmodel=medium -qopenmp -shared-intel -qopt-streaming-stores always -xCORE-AVX512 -qopt-zmm-usage=high`

output:
```
Function    Best Rate MB/s  Avg time     Min time     Max time

Copy:          426767.7     0.010655     0.010064     0.030492

Scale:         296451.9     0.014911     0.014488     0.023460

Add:           337654.4     0.019967     0.019080     0.037192

Triad:         340349.9     0.019685     0.018929     0.032305
```


inside tmux
0-31, 64-95

vs outside: 0-127

instead:
taskset -pc 0-127 \$$
numactl -s


best results so far:
triad with 64 threads, 0 offset, cores, spread
add with 64 threads, 0 offset cores, close
scale with 128 threads, 64 offset, cores, close
copy with 128 threads, 0 offset, threads, spread


baffling: -DSTREAM_TYPE=float 
```
Function    Best Rate MB/s  Avg time     Min time     Max time

Copy:          415857.2     0.005375     0.005164     0.009668

Scale:         366841.3     0.006781     0.005854     0.006921

Add:           472804.9     0.006939     0.006813     0.010852

Triad:         472799.2     0.006904     0.006813     0.010370
```
add and triad are significantly better, scale sucks (why?? it's just less work than triad??)


## best so far: 
export OMP_NUM_THREADS=128
export OMP_PLACES=cores
export OMP_PROC_BIND=spread
icx stream.c -o streamc.exe -DNTIMES=100 -DOFFSET=64 -DSTREAM_TYPE=float -DSTREAM_ARRAY_SIZE=268435456 -Wall -mcmodel=medium -qopenmp -shared-intel -qopt-streaming-stores=always -xCORE-AVX512 -qopt-zmm-usage=high
```
Function    Best Rate MB/s  Avg time     Min time     Max time

Copy:          461822.4     0.004852     0.004650     0.007329

Scale:         447869.0     0.005116     0.004795     0.011658

Add:           470109.1     0.007200     0.006852     0.017428

Triad:         470250.2     0.007168     0.006850     0.015198
```

I haven't been able to replicate these results, though. 

Another result with same settings: 
```
Function    Best Rate MB/s  Avg time     Min time     Max time

Copy:          438091.0     0.005127     0.004902     0.008242

Scale:         456335.5     0.005042     0.004706     0.011582

Add:           466572.1     0.007796     0.006904     0.065482

Triad:         472384.6     0.007358     0.006819     0.025022
```

### Using Intel Memory Latency Checker
Within this same directory (`~Applications/STREAM/STREAM stuff`), run `./Linux/mlc`
```
Measuring Peak Injection Memory Bandwidths for the system

Bandwidths are in MB/sec (1 MB/sec = 1,000,000 Bytes/sec)

Using all the threads from each core if Hyper-threading is enabled

Using traffic with the following read-write ratios

ALL Reads        : 544389.2

3:1 Reads-Writes : 494637.9

2:1 Reads-Writes : 489693.1

1:1 Reads-Writes : 486008.7

Stream-triad like: 454088.5
```
So if we trust this, I think we can conclude that our stream triad result is pretty good. 