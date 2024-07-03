################################ 
# WinterYetiy 
# Python-SystemCheckPC-v30.py
# Date: July 3, 2024
# Version: 3.0
# Description: A python program that checks the user's computer for basic statistics on CPU usage,
# memory, disk usage and battery power. The program looks for CPU temp as well, but the script does
# automatically work on Windows machines. It would have to be placed in the correct folder and run
# with administrator rights.
################################

#importing of necessary libraries
import psutil
import platform
import os

#look for CPU sensor check depending OS present
def get_cpu_temp():
    if platform.system() == "Linux":
        try:
            import subprocess
            result = subprocess.run(['sensors'], stdout=subprocess.PIPE)
            return result.stdout.decode('utf-8')
        except Exception as e:
            return str(e)
    elif platform.system() == "Windows":
        try:
            import clr  # pythonnet
            import wmi

            # Load the OpenHardwareMonitor library
            dll_path = os.path.join(os.getcwd(), "OpenHardwareMonitorLib.dll")
            clr.AddReference(dll_path)

            from OpenHardwareMonitor import Hardware

            # Initialize the Computer class
            computer = Hardware.Computer()
            computer.CPUEnabled = True
            computer.Open()

            temps = []
            for hardware in computer.Hardware:
                if hardware.HardwareType == Hardware.HardwareType.CPU:
                    hardware.Update()
                    for sensor in hardware.Sensors:
                        if sensor.SensorType == Hardware.SensorType.Temperature:
                            temps.append(f"{sensor.Name}: {sensor.Value} °C")
            return "\n".join(temps) if temps else "CPU temperature sensor not found."
        except Exception as e:
            return str(e)
    else:
        return "Unsupported operating system."

#system output results to user
def get_system_info():
    system_info = {
        "CPU Usage": f"{psutil.cpu_percent(interval=1)}%",
        "Memory Usage": f"{psutil.virtual_memory().percent}%",
        "Disk Usage": f"{psutil.disk_usage('/').percent}%",
        "Battery": f"{psutil.sensors_battery().percent}%" if psutil.sensors_battery() else "No battery"
    }
    return system_info

def main():
    print("System Information:")
    for key, value in get_system_info().items():
        print(f"{key}: {value}")
    
    print("\nCPU Temperature:")
    print(get_cpu_temp())

if __name__ == "__main__":
    main()

#end program
