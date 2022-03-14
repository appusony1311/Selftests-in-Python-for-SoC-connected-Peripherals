import os.path
import pandas as pd

thermal_path = "thermal_mon.txt"
cpu_clock_path = "current_cpu_clock.txt"


def therman_mon(filepath):
    abs_curdir = os.path.abspath(os.path.curdir)
    abs_filepath = os.path.join(abs_curdir, filepath)
    data = pd.read_csv(abs_filepath, sep=",", header=None)
    format_specs = "{: <7} {: <7} {: <7} {: <7} {: <7} {: <7}"
    print("Termal Monitor Stats:")
    print(format_specs.format("STAT", "PHY", "CPU0", "CPU1", "CPU2", "CPU3"))
    print(format_specs.format("MIN:",
                              min(data[0][1:]),
                              min(data[1][1:]),
                              min(data[2][1:]),
                              min(data[3][1:]),
                              min(data[4][1:])))

    print(format_specs.format("MAX:",
                              max(data[0][1:]),
                              max(data[1][1:]),
                              max(data[2][1:]),
                              max(data[3][1:]),
                              max(data[4][1:])))
    print("")


def cpu_clock_mon(filepath):
    abs_filepath = os.path.join(os.path.curdir, filepath)
    data = pd.read_csv(abs_filepath, sep=",", header=None)
    format_specs = "{: <10} {: <10} {: <10} {: <10} {: <10}"
    print("CPU Clock Stats:")
    print(format_specs.format("MIN:",
                              min(data[0][1:]),
                              min(data[1][1:]),
                              min(data[2][1:]),
                              min(data[3][1:])))
    print(format_specs.format("MAX:",
                              max(data[0][1:]),
                              max(data[1][1:]),
                              max(data[2][1:]),
                              max(data[3][1:])))
    print("")

therman_mon(thermal_path)
cpu_clock_mon(cpu_clock_path)
