## **System Health Monitor - CLI & GUI**

---

## **📌 Overview**
The **System Health Monitor** is a **real-time system diagnostics tool** designed to analyze and report **CPU, GPU, and WiFi stability and performance**.  

### **🛠️ Key Features**
✅ **CPU Health Check** – Monitors CPU stability, usage, and potential failures.  
✅ **GPU Health Check** – Analyzes GPU load, power consumption, and potential overheating risks.  
✅ **WiFi Stability Check** – Tests network latency, packet loss, and connection stability.  
✅ **Threaded Execution** – Runs tests without UI freezing or CLI interruptions.  
✅ **Admin Privilege Checks** – Prevents unauthorized access to sensitive data.  
✅ **Modern PyQt6 GUI** – User-friendly interface (GUI version).  
✅ **Efficient CLI Mode** – Lightweight, terminal-based interface (CLI version).  

### **🎯 Use Cases**
- **System Diagnostics** – Identify potential hardware failures before they happen.  
- **Performance Monitoring** – Ensure CPU, GPU, and network performance is optimal.  
- **Troubleshooting** – Detect overheating, instability, or connection issues.  

---

## **⚙️ How It Works**
The program collects **real-time system data** using **Python libraries** like `psutil`, `GPUtil`, and `ping3`. Each system component is analyzed using specific metrics to determine **health, failure rate, and stability**.

### **1️⃣ CPU Health Check**
- Uses `psutil.cpu_percent(interval=1)` to measure CPU load.
- Runs over a user-defined duration to calculate **CPU stability**:
  ```python
  avg_usage = sum(cpu_readings) / len(cpu_readings)
  max_deviation = max(abs(x - avg_usage) for x in cpu_readings)
  stability_ratio = max(0, 100 - max_deviation)
  ```
- **Fail Rate Calculation**:
  - High CPU usage (>80%) increases the fail rate.
  - Low stability (<50%) adds additional risk.
  - A normal usage pattern keeps fail rate **low**.

### **2️⃣ GPU Health Check**
- Uses `GPUtil.getGPUs()` to fetch GPU statistics.
- Monitors **GPU Load (%)** and **Power Consumption (Watts)**.
- If GPU power exceeds **200W**, it's flagged as **high risk**.
  ```python
  if gpu_power > 200:
      fail_rate += 30
      issues.append("High GPU power draw - Possible driver issues.")
  ```
- The system **disables GPU checks** if not run as an **Administrator**.

### **3️⃣ WiFi Stability Check**
- Sends multiple pings (`ping("8.8.8.8")` & `ping("1.1.1.1")`).
- Measures **latency**, **packet loss**, and **network stability**.
- The **stability formula**:
  ```python
  stability_rate = max(0, min(100, round(100 - avg_ping / 2, 2)))
  ```
- Detects potential **ISP issues, weak connections, or high jitter**.

### **4️⃣ Background Threads for Non-Blocking Execution**
The **GUI and CLI versions** use **Python threads** to ensure **continuous execution** without freezing the interface:
```python
def run_check(check_func, args=None):
    thread = threading.Thread(target=check_func, args=args if args else ())
    thread.start()
    return thread
```

---

## **🔌 How It Interacts with the System**
- Uses **`psutil`** for CPU metrics and system-wide statistics.
- Reads **GPU data** using **`GPUtil`** (requires admin rights on some OS).
- Uses **ICMP requests** (`ping3.ping`) to test **network reliability**.
- **Does not modify** system files, settings, or hardware.
- Runs in **user mode**, but requires **Admin privileges** for **full GPU checks**.

---

## **📥 Installation & Setup**
### **1️⃣ Prerequisites**
- **Python 3.8+**
- Required dependencies:  
  ```
  psutil
  GPUtil
  ping3
  PyQt6 (GUI only)
  ```

### **2️⃣ Install Required Libraries**
Run:
```sh
pip install psutil GPUtil ping3 PyQt6
```

### **3️⃣ Run the CLI Version**
```sh
python sys_health_mon_CLI.py
```

### **4️⃣ Run the GUI Version**
```sh
python sys_health_mon_GUI.py
```

### **5️⃣ (Optional) Run with Admin Privileges**
#### **Windows**
Right-click **Command Prompt (cmd)** → **Run as Administrator** → Execute script.

#### **Linux/macOS**
Run:
```sh
sudo python sys_health_mon_CLI.py
```

---

## **🛡️ Code Safety & Legal Guidelines**
### **1️⃣ Code Safety**
- **Read-Only Access** – The program **does not modify** system settings or hardware.
- **No Persistent Data Storage** – All data is collected **in real-time** without logs.
- **Thread-Safe Execution** – Uses **background threads** to prevent system hangs.
- **Fails Gracefully** – Detects permission issues and **avoids crashes**.

### **2️⃣ Legal & Ethical Guidelines**
- **Personal Use Only** – Do **not** use this program for **unauthorized monitoring**.
- **Admin Privileges** – Some functions require **elevated permissions** to access **system data**.
- **Network Monitoring** – Ensure compliance with **local laws** before running network tests.
- **Open Source Libraries** – This software relies on **publicly available** Python modules.

---

## **⚠️ Disclaimer**
**This tool is provided "as is" without warranty of any kind.** The author is **not responsible** for any system issues, data loss, or performance impacts caused by using this software. Use it at **your own risk**.  

- Running as **Administrator** may expose **sensitive system information**.  
- **Do not** run on **unauthorized** systems.  
- The tool **does not modify** system settings, but **misuse** could violate **organizational policies**.  