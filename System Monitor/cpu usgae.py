import psutil
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Create a figure and an axis for the graph
fig, ax = plt.subplots()

# Create a list to store CPU usage data
cpu_usage = []

# Define a function to monitor CPU usage
def monitor_cpu():
    cpu_percent = psutil.cpu_percent(interval=1)
    return cpu_percent

# Define a function to update the graph
def update_graph(frame):
    cpu_percent = monitor_cpu()
    cpu_usage.append(cpu_percent)
    ax.clear()
    ax.plot(cpu_usage)
    ax.set_ylim([0, 100])
    ax.set_title("CPU Usage")
    ax.set_xlabel("Time")
    ax.set_ylabel("CPU Usage (%)")

# Set up an animation to update the graph every 1 second
ani = animation.FuncAnimation(fig, update_graph, interval=1000)

# Display the graph
plt.show()
