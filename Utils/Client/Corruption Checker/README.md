# **Ultimate File Corruption Checker**
**Corruption Checker** is a powerful **Python-based** tool designed to detect, analyze, and attempt recovery of **corrupt files** in both **GUI** and **CLI** formats.  

With **advanced validation techniques**, it checks for **syntax errors**, **encoding issues**, **damaged archives**, **corrupt binaries**, and **more** while providing **detailed reports** and **auto-recovery mechanisms**.

---

## **📌 Features**
✅ **Supports Both CLI & GUI** - Choose between a command-line interface or a user-friendly graphical UI.  
✅ **Advanced Corruption Detection** - Analyzes text, images, PDFs, source code, and binary files.  
✅ **Syntax Validation for Source Code** - Detects errors in **Python, Java, and C++** files.  
✅ **Auto-Recovery System** - Creates **backup copies** and attempts to restore corrupted files.  
✅ **Recursive Folder Scanning** - Checks **all subdirectories** when analyzing a folder.  
✅ **Color-Coded Severity Levels** - Warnings, errors, and information are clearly distinguished.  

---

# **📦 Installation**
## **1️⃣ Prerequisites**
Ensure you have **Python 3.8+** installed:  
```bash
python --version
```
If Python isn't installed, download it from [python.org](https://www.python.org/downloads/).

## **2️⃣ Install Dependencies**
Install required Python packages using **pip**:  
```bash
pip install -r requirements.txt
```

### **📜 `requirements.txt`**
```
PyQt6
chardet
PyPDF2
Pillow
termcolor
```

---

# **🚀 Usage Guide**
## **🔹 Running the CLI Version (`corruption_checker_CLI.py`)**
Use the **command-line tool** to scan a **single file** or a **full directory**.

### **1️⃣ Check a Single File**
```bash
python corruption_checker_CLI.py -f /path/to/file.txt
```

### **2️⃣ Check an Entire Folder (Recursively)**
```bash
python corruption_checker_CLI.py -d /path/to/folder
```

### **3️⃣ Example Output**
```bash
Checking: /path/to/folder/example.py
Syntax error in Python file: example.py
Backup created: example.py.bak
Recovered file: example.py
Total Files Scanned: 15
Corruption Ratio: 13.33%
```

✅ **Color-coded output** helps differentiate **errors**, **warnings**, and **info** messages.

---

## **🔹 Running the GUI Version (`corruption_checker_GUI.py`)**
The **Graphical User Interface** provides an **intuitive** way to select files and scan them.

### **1️⃣ Start the GUI**
```bash
python corruption_checker_GUI.py
```

### **2️⃣ How to Use**
1. Click **"Select File"** to check a single file.  
2. Click **"Select Folder"** to scan an entire directory (including subfolders).  
3. The progress bar shows scanning status.  
4. **Results are displayed with colored severity indicators**.  

---

# **📖 How It Works**
### ✅ **Corruption Detection Methods**
1️⃣ **Source Code Validation**  
- Runs **Python syntax checks** (`py_compile`)  
- Runs **Java (`javac`) and C++ (`g++`) syntax validation**  
- Detects **empty files** or **malformed structures**  

2️⃣ **Text File Analysis**  
- Uses **chardet** to detect encoding errors  
- Identifies **malformed JSON/XML**  

3️⃣ **Image Validation**  
- Opens **JPG, PNG, GIF** with Pillow  
- Detects **corrupt pixels** or **truncated images**  

4️⃣ **PDF Validation**  
- Attempts to read PDF pages using `PyPDF2`  

5️⃣ **Archive Integrity Check**  
- Opens **ZIP/TAR** to detect errors  

6️⃣ **Binary File Hashing**  
- Computes **SHA-256 hash** to check for corruption  

---

# **🔄 Auto-Recovery Mechanism**
### **🔹 How It Works**
1. If a **corrupt source code or text file** is detected, a **backup is created**:  
   - Example: `example.py.bak`
2. The tool **filters out corrupt parts** (e.g., null-byte errors).  
3. If **recovery is successful**, the file is restored.  

💡 **Recovered files keep as much original content as possible!**

---

# **🛠 Troubleshooting**
### **1️⃣ PyQt6 Not Found?**
```bash
ModuleNotFoundError: No module named 'PyQt6'
```
💡 **Solution:** Install it manually:  
```bash
pip install PyQt6
```

### **2️⃣ `termcolor` Not Found in CLI?**
```bash
ModuleNotFoundError: No module named 'termcolor'
```
💡 **Solution:** Install it manually:  
```bash
pip install termcolor
```

### **3️⃣ Corrupt Files Not Recovering?**
- **Check the backup (`.bak`) file.**  
- **Use a text editor to inspect corrupted content.**  
- **Some files (e.g., binary) cannot be auto-recovered.**

---

# **📜 File Structure**
```
📂 corruption_checker/
│── corruption_checker_GUI.py  # Graphical Interface
│── corruption_checker_CLI.py  # Command-Line Interface
│── requirements.txt           # Dependencies
│── README.md                  # Documentation
```

---

# **💡 Future Improvements**
🔹 **More file formats supported (MP3, MP4, DOCX, etc.)**  
🔹 **Advanced AI-based corruption detection**  
🔹 **Logging system for saving reports**  

---

# **🔗 Credits & License**
✅ **Developed by:** [Your Name]  
✅ **License:** MIT (Free for everyone!)  

🔗 **Have suggestions?** Open an **issue or pull request**! 🚀  