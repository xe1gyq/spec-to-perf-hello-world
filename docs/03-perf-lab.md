# 03 — Hello, Linux perf

## Setup

Install GCC, Make, Python 3, and your distribution's Linux perf package.
For example, Fedora/CentOS/RHEL commonly provide `perf` via `sudo dnf install perf`.
Ubuntu packages depend on the running kernel (commonly `linux-tools-common` and
`linux-tools-$(uname -r)`). Use your distribution's package instructions if unavailable.

```sh
command -v gcc make python3 perf
perf --version
make test
```

## Step 1: understand the work

For a 4 × 4 matrix, rows read linear indices `0,1,2,3,4,...`; columns start
`0,4,8,12,1,5,...`. Both add exactly the same values. At larger sizes, the order
can change how effectively the CPU cache supplies data.

```sh
make demo
```

`elapsed_seconds` measures traversal only. Small runs may round to zero.

## Step 2: count events

```sh
perf stat -r 5 -e task-clock,cycles,instructions,cache-references,cache-misses -- ./build/matrix-scan row 2048 20
perf stat -r 5 -e task-clock,cycles,instructions,cache-references,cache-misses -- ./build/matrix-scan column 2048 20
```

`perf stat` reports aggregate measurements for the whole process, including
allocation and initialization. `-r 5` repeats the process five times. Cycles and
instructions describe CPU work; cache events give additional clues when supported.
Generic cache events have hardware-specific meanings; do not label them all L1 misses.

## Step 3: find a hot function

```sh
mkdir -p results
perf record -e cpu-clock:u -F 99 -g -o results/column.data -- ./build/matrix-scan column 2048 100
perf report --stdio -i results/column.data
perf annotate --stdio -i results/column.data --symbol sum_columns
```

Recording samples asks where execution was spending time. Look for `sum_columns`;
its presence and sample share must be verified on your run. Debug symbols (`-g` in
GCC) help relate addresses to source; frame pointers support call stacks. In the
`perf record` command, `-g` instead means record call graphs. `cpu-clock:u` samples
user-space CPU time and does not require a hardware cycles counter, but still
requires permission to profile.

`make profile` collects the main commands, environment, and reports automatically.
It stops on errors instead of reporting an incomplete profile as successful.

## Step 4: interpret cautiously

Record CPU, kernel, compiler, flags, input size, repetitions, and other system load.
Compare repeated runs, alternate mode order, and increase repetitions if runs are too short.
Try sizes 256, 1024, 2048, and 2049; cache capacity and stride can both affect results.
An observed ratio is `column time / row time`; do not mix internal and perf elapsed times.
A speed difference alone does not prove cache misses caused it. Sampling is statistical.

## When perf is unavailable

- Missing command: install the distribution's matching perf package.
- Permission error: inspect `cat /proc/sys/kernel/perf_event_paranoid` and consult your administrator or use a permitted development host. Do not silently change system policy.
- Unsupported hardware events: try `perf stat -r 5 -e task-clock -- ./build/matrix-scan row 2048 20`, then column. This measures CPU time, not cache misses.
- Containers or VMs may restrict both software and hardware events. Use the built-in timer and explicitly record that hardware-counter analysis is pending.

## Official references

- [Linux perf stat documentation](https://github.com/torvalds/linux/blob/master/tools/perf/Documentation/perf-stat.txt)
- [Linux perf record documentation](https://github.com/torvalds/linux/blob/master/tools/perf/Documentation/perf-record.txt)
- [Linux kernel workload tracing guide](https://docs.kernel.org/admin-guide/workload-tracing.html)
