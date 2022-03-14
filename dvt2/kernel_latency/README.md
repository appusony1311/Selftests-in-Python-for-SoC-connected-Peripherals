# Kernel Latency Test
---

## Precondition
You need to install `gnuplot` application. Run: `sudo apt-get install gnuplot`.

## Concepts
The main concepts to understand Kernel benchmarks could be found [here](https://confluence.bln.native-instruments.de/display/DEV/Real-Time+kernel+tests).

## Setup
You should run this test on a debug image.

## External variables

* CPU --> How many CPU cores the system has. Default is `CPU=4`.
* IO --> How many stress IO workers you need. Default is `IO=4`.
* VM --> How many stress RAM memory workers you need. Default is `VM=4`.
* HDD --> How many stress HDD workers you need. Default is `HDD=1`.
* HDD-BYTES --> Size of writing blocks of a HDD worker. Default is `HDD-BYTES=256M`.
* LONG --> How long the test should last in minutes. Default is `LONG=720`.

## Run
Go to this folder `qa\kernel_latency`

Run `[EXTERNAL VARIABLES] ./worst_case_scenario.sh`.
e.g.:
* `LONG=720 ./worst_case_scenario.sh`.

## Outcome
The resulting files will be store in the `benchmark_test` folder. It will be packaged in a tar.gz file.
The main file is `cyclictest_output.txt`. It is a cyclictest histogram.

## Generating the graph
You should use the `cyclictest_output_process.sh`, you need to locate the `benchmark_test` folder in the same folder of this script.
It will create a `png` plot.

OBS: You could not run `cyclictest_output_process.sh` on the Q7 board. You should run in your host computer (e.g. Ubuntu).

---

## Using ftrace and cyclictest to trace Kernel high latency

## Precondition

The NativeOS should have the below Kernel flags enabled in order to use it. That is the requirements until 04/Oct/2018 (see Links):

* CONFIG_FTRACE=y
* CONFIG_FUNCTION_TRACER=y
* CONFIG_FUNCTION_GRAPH_TRACER=y
* CONFIG_SCHED_TRACER=y
* CONFIG_FTRACE_SYSCALLS=y
* CONFIG_STACK_TRACER=y
* CONFIG_DYNAMIC_FTRACE=y
* CONFIG_FUNCTION_PROFILER=y
* CONFIG_DEBUG_FS=y
* CONFIG_IRQSOFF_TRACER=y
* CONFIG_PREEMPT_TRACER=y

To verify if all these flags are enabled in the system under the test, you can run:

`cat /proc/config.gz | gunzip | egrep -w 'CONFIG_FTRACE|CONFIG_FUNCTION_TRACER|CONFIG_FUNCTION_GRAPH_TRACER|CONFIG_SCHED_TRACER|CONFIG_FTRACE_SYSCALLS|CONFIG_STACK_TRACER|CONFIG_DYNAMIC_FTRACE|CONFIG_FUNCTION_PROFILER|CONFIG_DEBUG_FS|CONFIG_IRQSOFF_TRACER|CONFIG_PREEMPT_TRACER'`

The expected output should be:

`CONFIG_DEBUG_FS=y`
`CONFIG_FTRACE=y`
`CONFIG_FUNCTION_TRACER=y`
`CONFIG_FUNCTION_GRAPH_TRACER=y`
`CONFIG_IRQSOFF_TRACER=y`
`CONFIG_PREEMPT_TRACER=y`
`CONFIG_SCHED_TRACER=y`
`CONFIG_FTRACE_SYSCALLS=y`
`CONFIG_STACK_TRACER=y`
`CONFIG_DYNAMIC_FTRACE=y`
`CONFIG_FUNCTION_PROFILER=y`

The suffix `=y` should be present!

A easy way to verify if you the 11 entries (in this case) is run:
`cat /proc/config.gz | gunzip | egrep -w 'CONFIG_FTRACE|CONFIG_FUNCTION_TRACER|CONFIG_FUNCTION_GRAPH_TRACER|CONFIG_SCHED_TRACER|CONFIG_FTRACE_SYSCALLS|CONFIG_STACK_TRACER|CONFIG_DYNAMIC_FTRACE|CONFIG_FUNCTION_PROFILER|CONFIG_DEBUG_FS|CONFIG_IRQSOFF_TRACER|CONFIG_PREEMPT_TRACER' | wc -l`
You should get `11`.

Once ftrace is properly enabled, you should be able to access the debugfs located in `/sys/kernel/debug`.


## Using ftrace with cyclictest in the worst_case_scenario.sh script

When you need to trace it, you should use the argument `-b [TRACEPOINT INTEGER]`, e.g.:
`./worst_case_scenario.sh -b 2000`, in this example, the cyclictest will run alongside with ftrace with trace breakpoint of 2000 us. It means, the cyclictest will be closed if the latency is greater than that is found.

Once the tracebreak is reached, it will include in the cyclictest output file the high latency thread number, e.g.:

`# Thread Ids: 04960 04961`
`# Break thread: 4960`

The max latency could be found on:
`/benchmark_test/max_latency_output` or `/benchmark_test/cyclictest_output.txt`

Now, you are ready to extract the trace data using:
`cat /sys/kernel/debug/tracing/trace > tracedata.txt`

The `tracedata.txt` should be enough to identify which Kernel call is causing the high latency. Ideally, this data should be analised by someone with expertise in that domain. Tim Blechmann would be a good candidate.

Be aware that enabling ftrace introduces a lot of latency. For the real latency, you should run the script without running ftrace.


### Link

[Finding Realtime Linux Kernel Latencies](https://people.redhat.com/williams/latency-howto/rt-latency-howto.txt)
[FTrace Documentation](https://rt.wiki.kernel.org/index.php/Ftrace)
[Cyclictest manpages](https://manpages.debian.org/jessie/rt-tests/cyclictest.8.en.html)