import matplotlib.pyplot as plt
import generateNOC
injectionRates = [i/200 for i in range(1, 101)]
aLatency = []
mLatency = []
for injectionRate in injectionRates:
    latency = generateNOC.getLatency(injectionRate)
    aLatency.append(latency[0])
    mLatency.append(latency[1])
    print(latency)
plt.plot(injectionRates, aLatency, label="Average Latency")
plt.plot(injectionRates, mLatency, label="Max Latency")
plt.xlabel('Injection Rate')
plt.ylabel('Latency')
plt.legend()
plt.show()
