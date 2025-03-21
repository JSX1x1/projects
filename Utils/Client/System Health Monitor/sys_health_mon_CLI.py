import os
import psutil
import GPUtil
import ctypes
import time
import threading
from ping3 import ping

def is_admin():
    try:
        return os.geteuid() == 0  
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0  

def get_cpu_stability(duration):
    """ Measures CPU stability based on usage fluctuations over time """
    cpu_readings = []
    for _ in range(duration):
        cpu_readings.append(psutil.cpu_percent(interval=1))
    
    avg_usage = sum(cpu_readings) / len(cpu_readings)
    max_deviation = max(abs(x - avg_usage) for x in cpu_readings)
    stability_ratio = max(0, 100 - max_deviation)

    return round(stability_ratio, 2)

def calculate_fail_rate(usage, stability, component):
    fail_rate = 0
    issues = []

    if usage > 80:
        fail_rate += 30
        issues.append(f"High {component} usage ({usage}%) - Close unused apps.")

    if stability < 50:
        fail_rate += 40
        issues.append(f"Unstable {component} performance ({stability}% stability) - Possible CPU/GPU throttling.")

    if usage < 80 and stability >= 50:
        fail_rate = 10  

    fail_rate = max(0, min(100, fail_rate))
    return fail_rate, ", ".join(issues) if issues else "No major issues detected."

def check_cpu(duration):
    print("\n[Checking CPU Health...]\n")
    stability_ratio = get_cpu_stability(duration)
    cpu_usage = psutil.cpu_percent(interval=1)
    fail_rate, issues = calculate_fail_rate(cpu_usage, stability_ratio, "CPU")
    health_rate = 100 - fail_rate

    print(f"CPU Health: {health_rate}% | Fail Rate: {fail_rate}%")
    print(f"Stability: {stability_ratio}%")
    print(f"Issues: {issues}\n")

def check_gpu():
    print("\n[Checking GPU Health...]\n")
    try:
        gpus = GPUtil.getGPUs()
        if not gpus:
            print("No GPU detected.\n")
            return
        gpu = gpus[0]
        gpu_usage = gpu.load * 100
        gpu_power = gpu.powerUsage
        fail_rate, issues = calculate_fail_rate(gpu_usage, gpu_power, "GPU")
        health_rate = 100 - fail_rate

        print(f"GPU Health: {health_rate}% | Fail Rate: {fail_rate}%")
        print(f"Issues: {issues}\n")
    except:
        print("GPU check failed (Run as Admin).\n")

def check_wifi():
    print("\n[Checking WiFi Stability...]\n")
    ping_google = ping("8.8.8.8") or 100
    ping_cloudflare = ping("1.1.1.1") or 100
    avg_ping = round((ping_google + ping_cloudflare) / 2, 2)
    stability_rate = max(0, min(100, round(100 - avg_ping / 2, 2)))

    issues = []
    if avg_ping > 100:
        issues.append("High latency - check your connection.")
    if stability_rate < 50:
        issues.append("Unstable network - possible packet loss.")

    issues_text = ", ".join(issues) if issues else "No major issues detected."
    print(f"WiFi Stability: {stability_rate}%")
    print(f"Issues: {issues_text}\n")

def run_check(check_func, args=None):
    thread = threading.Thread(target=check_func, args=args if args else ())
    thread.start()
    return thread

if __name__ == "__main__":
    print("System Health Monitor - CLI Version")
    print("===================================")

    while True:
        print("\nOptions:")
        print("1. Check CPU Health")
        print("2. Check GPU Health")
        print("3. Check WiFi Stability")
        print("4. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            duration = int(input("Enter monitoring duration (seconds): "))
            run_check(check_cpu, (duration,))
        elif choice == "2":
            run_check(check_gpu)
        elif choice == "3":
            run_check(check_wifi)
        elif choice == "4":
            print("Exiting System Health Monitor.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")
