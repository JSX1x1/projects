## **File System Structure Analyzer (CLI & GUI)**  
### *A Powerful Educational Tool for Understanding File System Structures*  

---

## **📌 About the Tool**  

The **File System Structure Analyzer** is an **educational utility** designed to help users **understand and explore file system structures**. It comes in **two versions**:  

1. **CLI Version** – A terminal-based version for lightweight usage.  
2. **GUI Version (PyQt6)** – A visually interactive interface with a modern theme.  

This tool **does not modify** or alter any files or structures; it only **retrieves and displays** file system details for **educational and diagnostic purposes**.  

### **🌟 Features**  
✅ Detects **available drives** (USB, SSD, HDD).  
✅ Displays **file system types** (NTFS, FAT32, EXT4, etc.).  
✅ Shows **used/free space, mount points, and partition details**.  
✅ **Admin Mode** unlocks **advanced insights** (sector details, journaling info, NTFS metadata, etc.).  
✅ **Cross-platform** (Windows, Linux, MacOS).  

---

## **📖 How to Use**  

### **CLI Version**  
1. Open a terminal and navigate to the tool’s directory.  
2. Run the CLI tool using Python:  
   ```sh
   python file_sys_struct_analyser_CLI.py
   ```
3. Select a drive from the list to analyze.  
4. The tool will display the file system details.  

💡 **If running as an administrator/root, additional details will be available.**  

### **GUI Version (PyQt6)**  
1. Open a terminal and navigate to the tool’s directory.  
2. Run the GUI tool using Python:  
   ```sh
   python file_sys_struct_analyser_GUI.py
   ```
3. The modern PyQt6 interface will open, showing available drives.  
4. Click on a drive to analyze its file system details.  
5. **Admin mode unlocks advanced insights!**  

---

## **🛠 Installation & Setup**  

### **🔹 Prerequisites**  
Ensure you have **Python 3.8+** installed. If not, download it from [python.org](https://www.python.org/).  

### **🔹 Install Required Dependencies**  
Run the following command to install the required Python packages:  
```sh
pip install psutil PyQt6
```

### **🔹 Run the Analyzer**  
CLI Version:  
```sh
python file_sys_struct_analyser_CLI.py
```
GUI Version:  
```sh
python file_sys_struct_analyser_GUI.py
```

✅ **You're ready to analyze file systems!**  

---

## **🛡 Safety Guidelines & Hints**  

⚠ **Always verify scripts before running them, especially with admin/root access.**  
⚠ **This tool only reads file system structures and does NOT modify any data.**  
⚠ **Running as admin/root will expose deeper system information—use responsibly.**  
⚠ **Do not analyze critical system drives unless necessary.**  
⚠ **Avoid using this tool on unknown USB drives for security reasons.**  

**Tip:** Running the GUI version as a normal user ensures restricted access to **only safe, non-critical** information.  

---

## **⚠ DISCLAIMER**  

> **This tool is strictly for educational and diagnostic purposes.**  
> **It does not alter, modify, or damage any data.**  
> Unauthorized usage to access **protected system files or critical infrastructures** may violate legal policies.  
> The developer is **not responsible** for any misuse or unintended consequences of running this tool.  
> Always ensure you have **proper permissions** before running system analysis tools.  