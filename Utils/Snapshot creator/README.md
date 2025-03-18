Here's a **fully professional README** for your tool, covering both the GUI and CLI versions. It includes:  

✅ **Project Overview**  
✅ **Features**  
✅ **Installation** (step-by-step)  
✅ **Usage Instructions** (GUI & CLI)  
✅ **Technical Details**  
✅ **Future Improvements**  

---

## **📌 Snapshot Creator - GUI & CLI**  
A powerful tool for creating compressed snapshots of directories, analyzing file corruption risks, and excluding unnecessary files.  

---

## **📖 Table of Contents**  
1. [Project Overview](#project-overview)  
2. [Features](#features)  
3. [Installation](#installation)  
4. [Usage](#usage)  
   - [GUI Version](#gui-version)  
   - [CLI Version](#cli-version)  
5. [Technical Details](#technical-details)  
6. [Future Improvements](#future-improvements)  

---

## **📜 Project Overview**  
The **Snapshot Creator** is a Python-based tool that allows users to:  
- Select a folder to create a **compressed ZIP snapshot**  
- Estimate the **size before and after compression**  
- Analyze **file corruption risks** and flag potentially problematic files  
- Identify **unnecessary files** (logs, caches, temp files)  
- Provide an **option to exclude risky/unnecessary files** from the ZIP  
- **Display real-time progress** during compression  

This tool is available in **both a GUI version (PyQt6)** and a **CLI version (command-line interface)** for flexible usage.  

---

## **🚀 Features**  
✅ User selects a folder for snapshot creation  
✅ **Estimated size** before and after compression  
✅ **Corruption risk detection** (flags unreadable files)  
✅ **Unnecessary file identification** (`.log`, `.tmp`, `.cache` files)  
✅ Option to **exclude flagged files** from compression  
✅ **Real-time progress bar**  
✅ Saves snapshots as `mm-dd-yyyy-snapshot.zip`  
✅ **Available in GUI and CLI versions**  

---

## **📥 Installation**  
### **1️⃣ Install Python**  
Ensure Python 3.8+ is installed on your system:  
```bash
python --version
```
If not installed, download it from [python.org](https://www.python.org/downloads/).  

### **2️⃣ Install Dependencies**  
Install the required Python packages:  
```bash
pip install -r requirements.txt
```
Or manually install them:  
```bash
pip install PyQt6
```

### **3️⃣ Download the Scripts**  
Clone this repository or manually download the scripts:  
```bash
git clone https://github.com/your-repo/snapshot-creator.git
cd snapshot-creator
```

---

## **📌 Usage**  
### **🖥 GUI Version**  
#### **Running the GUI**  
```bash
python snapshot_creator_GUI.py
```
#### **Step-by-Step Usage**  
1. Click **"Select Folder"** and choose a directory.  
2. The tool calculates:  
   - **Estimated original size**  
   - **Estimated compressed size**  
   - **Corruption risks** (unreadable files)  
   - **Unnecessary files** (cache, logs, etc.)  
3. Choose whether to **exclude risky/unnecessary files**.  
4. Click **"Create Snapshot"**.  
5. The **progress bar updates** as files are compressed.  
6. Once complete, the ZIP file is saved in the **parent directory** of the selected folder.  

---

### **🖥 CLI Version**  
#### **Basic Usage**  
```bash
python snapshot_creator_CLI.py "/path/to/folder"
```
#### **Optional Flags**  
| Flag | Description | Example |
|------|------------|---------|
| `--exclude-risky` | Excludes flagged risky files | `python snapshot_creator_CLI.py "/path/to/folder" --exclude-risky` |
| `--exclude-unnecessary` | Excludes unnecessary files | `python snapshot_creator_CLI.py "/path/to/folder" --exclude-unnecessary` |

#### **Interactive Mode**  
If no folder is provided, the script will ask for it:  
```bash
python snapshot_creator_CLI.py
```
It will then prompt:  
- **"Exclude risky files? (y/n)"**  
- **"Exclude unnecessary files? (y/n)"**  

#### **Progress Bar Example Output**  
```
Selected folder: /Users/example/Documents
Estimated Size: 512.34 MB
Estimated Compressed Size: 256.17 MB
Corruption Risk: 2 files
Unnecessary Files: 5 files
Exclude risky files? (y/n): y
Exclude unnecessary files? (y/n): y
Creating snapshot: /Users/example/Documents/03-18-2025-snapshot.zip
Progress: 75%
Snapshot creation complete.
Snapshot saved as: /Users/example/Documents/03-18-2025-snapshot.zip
```

---

## **🛠 Technical Details**  
- **Python 3.8+**  
- Uses `zipfile` for **compression**  
- Uses `os` and `pathlib` for **file operations**  
- Implements **multithreading** (GUI) for UI responsiveness  
- Real-time **progress updates**  

### **How Corruption Risk is Detected**  
- **Unreadable files**: If a file cannot be opened in read mode, it is flagged as risky.  

### **How Unnecessary Files Are Identified**  
- Common **cache/log/temp files** with extensions:  
  - `.log`, `.tmp`, `.cache`  