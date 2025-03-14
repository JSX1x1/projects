# **Advanced Disk Monitoring Tool**  

This document provides a **detailed step-by-step guide** for using the **Advanced Disk Monitoring Tool**. It includes **legal and safety disclaimers**, **usage rights**, and **important security considerations**.  

---

## **📌 Table of Contents**  
1️⃣ **Introduction**  
2️⃣ **Features & Capabilities**  
3️⃣ **Installation & Requirements**  
4️⃣ **How to Use the Tool (Step-by-Step Guide)**  
5️⃣ **Restrictions & Limitations**  
6️⃣ **Usage Rights & Legal Compliance**  
7️⃣ **Safety Precautions & Best Practices**  
8️⃣ **Frequently Asked Questions (FAQs)**  

---

# **1️⃣ Introduction**  

The **Advanced Disk Monitoring Tool** is a powerful **client-based utility** that provides deep insights into **disk storage, file distributions, and system details**. It is designed for **IT administrators, system analysts, and advanced users** to **analyze, troubleshoot, and monitor disk usage** in real-time.  

⚠️ **WARNING:**  
This tool requires **admin privileges** to access all features. If run without admin rights, some functionality will be **restricted** for security reasons.  

---

# **2️⃣ Features & Capabilities**  

✅ **Lists all available disks (HDDs, SSDs, USB drives)**  
✅ **Shows disk usage (total, used, free space)**  
✅ **File type distribution (Documents, Videos, System Files, etc.)**  
✅ **Reads disk SMART data (Health Status, Temperature, Errors) (Windows Only)**  
✅ **Detects partition and logical volume details**  
✅ **Checks disk type, filesystem, and serial number**  
✅ **Admin Privilege Detection (Prevents Unauthorized Access)**  

---

# **3️⃣ Installation & Requirements**  

## **💻 System Requirements**  
- **OS:** Windows 10/11, Linux, macOS  
- **Python Version:** **Python 3.8+**  
- **Admin Rights:** **Recommended for full access**  

## **📦 Install Required Dependencies**  
Before using the tool, install required Python packages:  
```sh
pip install pyqt6 psutil humanize wmi
```
(Windows users need `wmi`, while Linux/macOS users can use `smartmontools` for deep disk checks.)  

## **🛠️ Running the Tool**
1. Open **Command Prompt (CMD)** or **Terminal**.  
2. Navigate to the tool’s location:  
   ```sh
   cd path/to/disk_monitoring/
   ```
3. Run the program:  
   ```sh
   python disk_monitoring.py
   ```

---

# **4️⃣ How to Use the Tool (Step-by-Step Guide)**  

### **1️⃣ Open the Application**  
- If running **without admin privileges**, some features will be **disabled** for security reasons.  
- If running **as an admin**, full access is granted.  

---

### **2️⃣ Select a Disk**  
- A list of **all detected disks** will be displayed.  
- Click on a disk to **view detailed information**.  

---

### **3️⃣ View Disk Usage**  
Once a disk is selected, the tool will display:  
✅ **Total Disk Space**  
✅ **Used vs Free Space**  
✅ **File System Type (NTFS, FAT32, ext4, etc.)**  
✅ **Drive Serial Number & Partition Info**  

---

### **4️⃣ Scan File Type Distribution**  
- The tool will **scan all files** on the selected disk.  
- It will **categorize** files into **Documents, Images, Videos, System Files, etc.**  
- A **progress bar** will indicate scanning status.  

⚠️ **Note:** Large disks **may take several minutes** to scan.  

---

### **5️⃣ View Deep Disk Info (Windows Only)**  
- The tool will attempt to **read SMART data** (disk temperature, read/write errors, health status).  
- Some disks **may block access** to SMART data due to manufacturer settings.  

---

### **6️⃣ Refresh Disk List**  
- Click **“Refresh Disks”** if a new disk is connected.  
- This will reload the **disk list without restarting the tool**.  

---

# **5️⃣ Restrictions & Limitations**  

### **1️⃣ Admin Privileges Required for Full Access**  
🔹 If you **do not run the tool as admin**, it will:  
❌ Restrict access to **some system-level disk details**.  
❌ Disable **SMART data retrieval**.  
❌ Block **direct low-level disk access**.  

---

### **2️⃣ Cannot Modify or Delete Files**  
🔹 This tool is **read-only** and **cannot modify, delete, or move files**.  

---

### **3️⃣ Limited SMART Data Access**  
🔹 Some disks **block access** to SMART health details due to manufacturer settings.  

---

# **6️⃣ Usage Rights & Legal Compliance**  

⚠️ **IMPORTANT NOTICE: Unauthorized access to storage devices may be illegal!**  

## **✅ Permitted Uses**  
✔️ Personal use (analyzing your own disks)  
✔️ IT administration (managing company-approved systems)  
✔️ System troubleshooting & diagnostics  
✔️ Data compliance audits  

## **🚫 Prohibited Uses**  
❌ **Scanning unauthorized devices without permission**  
❌ **Attempting to bypass encryption or security restrictions**  
❌ **Using the tool for illegal surveillance or hacking**  

### **🔹 Legal References**
- **GDPR (Europe)** → [General Data Protection Regulation](https://gdpr.eu/)  
- **CCPA (California)** → [California Consumer Privacy Act](https://oag.ca.gov/privacy/ccpa)  
- **HIPAA (USA)** → [Health Insurance Portability and Accountability Act](https://www.hhs.gov/hipaa/index.html)  

🔹 **If in doubt, consult a legal expert before using this tool in a corporate or regulated environment.**  

---

# **7️⃣ Safety Precautions & Best Practices**  

## **✅ DO’s**  
✔️ **Run as Admin** for full functionality.  
✔️ **Use only on authorized devices.**  
✔️ **Regularly refresh the disk list** for real-time updates.  
✔️ **Close other disk-intensive apps** before scanning.  

## **❌ DON’Ts**  
❌ **Do not scan disks with sensitive data if you lack permission.**  
❌ **Do not attempt to modify disk contents using this tool.**  
❌ **Avoid scanning disks in use by another process.**  

---

# **8️⃣ Frequently Asked Questions (FAQs)**  

### **Q: Why can’t I see SMART data for my SSD?**  
🔹 Some SSD manufacturers **disable SMART access** for security reasons.  

### **Q: The tool is not detecting external USB drives.**  
✅ Try unplugging and reconnecting the USB device.  
✅ Click **"Refresh Disks"** to reload the disk list.  

### **Q: Why is scanning slow on large disks?**  
🔹 The tool **scans every file**, so larger disks take longer.  
🔹 Consider **excluding system files** for faster results.  

### **Q: Can I use this tool for forensic recovery?**  
❌ No, this tool **only analyzes available data** and **does not recover deleted files**.  

---

# **📜 Legal Disclaimer**  

🛑 **This tool is intended for lawful and ethical use only.**  
Unauthorized access, scanning, or monitoring of **storage devices without consent** may be **illegal** and could lead to criminal prosecution.  

By using this software, you accept full responsibility for ensuring compliance with **privacy laws, company policies, and legal regulations**.  

---

# **Conclusion**  
The **Advanced Disk Monitoring Tool** is a powerful utility for **analyzing disk usage, file types, and system health**.  

✅ **Use it for:**  
✔️ System monitoring & troubleshooting  
✔️ IT administration & compliance audits  
✔️ Managing disk storage efficiently  

⚠️ **Do NOT use it for:**  
❌ Unauthorized access to private storage  
❌ Modifying or deleting data on systems without permission  
❌ Hacking or surveillance  