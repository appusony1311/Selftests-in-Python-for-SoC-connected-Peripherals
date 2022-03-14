
CYCLICTEST_RESULT = "cyclictest_output.txt"

with open(CYCLICTEST_RESULT, 'r') as file:
    for line in file:
        if "Max Latencies" in line:
            max_latency = max(line.split()[3:])
            break

with open("max_latency_output", 'w') as file:
    file.write(max_latency)

print("MAX LATENCY --> {} us\n".format(max_latency))
