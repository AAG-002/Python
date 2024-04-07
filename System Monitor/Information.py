import platform
import psutil

#COMPUTER INFORMATION:
print("-------------------COMPUTER INFORMATION------------------------")
print(f"Computer Name: {platform.node()}")
print(f"Machine Type: {platform.machine()}")
print(f"Processor Type: {platform.processor()}")
print(f"Operating System: {platform.system()}")
print(f"Operating System Release: {platform.release()}")
print(f"Operating System Version: {platform.version()}")
print("")

#CPU INFORMATION:
print("---------------------CPU INFORMATION--------------------------")
print(f"Number of physical cores: {psutil.cpu_count(logical=False)}")
print(f"Number of logical cores: {psutil.cpu_count(logical=True)}")
print(f"Current CPU frequency: {round(psutil.cpu_freq().current/1000,2)}GHz")
print(f"Current CPU Utilization: {psutil.cpu_percent(interval=1)}%")
print(f"PER-CPU Utilization: {psutil.cpu_percent(interval=1,percpu=True)}")
print("")

#RAM INFORMATION:
print("---------------------RAM INFORMATION--------------------------")
print(f"Total RAM installed: {round(psutil.virtual_memory().total/1000000000,2)} GB")
print(f"Available RAM: {round(psutil.virtual_memory().total/1000000000,2)} GB")
print(f"Used RAM: {round(psutil.virtual_memory().used/1000000000,2)} GB")
print(f"Current RAM Usage: {psutil.virtual_memory().percent}%")
print("")

#STORAGE INFORMATION:
print("--------------------STORAGE INFORMATION------------------------")
print(f"Total Storage (excluding Windows): {round(psutil.disk_usage('/').total/1000000000,2)} GB")
print(f"Used Storage: {round(psutil.disk_usage('/').used/1000000000,2)} GB")
print(f"Available Storage: {round(psutil.disk_usage('/').free/1000000000,2)} GB")
print(f"Percentage Used: {psutil.disk_usage('/').percent}%")
print(f"")
