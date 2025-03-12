## **📜 TAR.GZ Unpacker - GUI & CLI Manual**  

### **Overview**  
This tool allows you to **extract `.tar.gz` archives** (commonly used on Linux) and optionally **convert them to `.zip`** for better compatibility on Windows.  

✅ **Extract `.tar.gz` archives**  
✅ **Convert extracted files to `.zip`**  
✅ **Simple GUI & CLI versions available**  
✅ **Works on Windows, macOS, and Linux**  

---

## **GUI Version (`tar_gz_unpacker_GUI.py`)**  

### **How to Run**
1. **Install dependencies** (if not already installed)  
   ```
   pip install PyQt6
   ```
2. **Run the GUI application**  
   ```
   python tar_gz_unpacker_GUI.py
   ```
3. **Steps to Extract & Convert**  
   - Click **"Choose File"** and select a `.tar.gz` file  
   - Click **"Extract .tar.gz"** to unpack the archive  
   - Click **"Convert Extracted Folder to .zip"** to create a ZIP file  

---

## **CLI Version (`tar_gz_unpacker_CLI.py`)**  

### **How to Run**
1. **Run the CLI application**  
   ```
   python tar_gz_unpacker_CLI.py --help
   ```
   *(Displays available commands and options.)*

2. **Extract a `.tar.gz` File**  
   ```
   python tar_gz_unpacker_CLI.py myfile.tar.gz
   ```
   - Extracts `myfile.tar.gz` into a folder named `myfile`  

3. **Extract & Convert to `.zip`**  
   ```
   python tar_gz_unpacker_CLI.py myfile.tar.gz --convert
   ```
   - Extracts `myfile.tar.gz` and **automatically converts** it into `myfile.zip`  

---

## **📊 Example CLI Output**
```
Extracting myfile.tar.gz to myfile...
Extraction completed! Files are in: myfile
Converting 'myfile' to ZIP...
Conversion completed! ZIP file saved as: myfile.zip
```

---

## **📌 Notes**
- The **GUI version** provides a **user-friendly** interface  
- The **CLI version** is great for **automating tasks**  
- Extracted files are stored in a folder with the same name as the archive  
- The **`--convert`** flag **automatically creates a `.zip`**  