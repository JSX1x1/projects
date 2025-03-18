# **File Recovery Tool (PyQt6)**  
This document provides a **detailed step-by-step guide** on how to use the **File Recovery Tool** effectively and safely.  

---

# **🔹 Table of Contents**
1️⃣ **Introduction**  
2️⃣ **How It Works**  
3️⃣ **Installation & Requirements**  
4️⃣ **How to Use the Tool (Step-by-Step)**  
5️⃣ **File Recovery Process Explained**  
6️⃣ **Safety Tips & Best Practices**  
7️⃣ **FAQs & Troubleshooting**  

---

# **1️⃣ Introduction**  
The **Advanced Deep File Recovery Tool** is a powerful program that allows you to **scan for deleted files** and **recover lost data** from your hard drive. It works by searching for file **signatures** (JPG, PNG, PDF, DOCX, etc.) within the **raw disk sectors**, allowing recovery even when the **Recycle Bin has been emptied**.  

✅ **Key Features:**  
- **Supports multiple file types:** JPG, PNG, PDF, DOCX, MP4, ZIP, and more.  
- **Deep disk scanning:** Finds files even after deletion.  
- **Admin Privilege Check:** Prevents unauthorized use.  
- **User-Friendly GUI:** Simple interface with drive selection, progress bar, and file list.  
- **No external dependencies:** Works without special drivers or tools.  

---

# **2️⃣ How It Works**  
🔍 **Deleted files are not immediately removed** from the hard drive. Instead, the system marks the space as "available," meaning the data still exists **until it gets overwritten**. This tool **scans raw disk sectors** for file signatures and attempts to reconstruct the files.  

---

# **3️⃣ Installation & Requirements**  

## **💻 System Requirements**
- **OS:** Windows 10/11 (Admin privileges recommended for full access)  
- **RAM:** Minimum **4GB RAM** for smooth scanning  
- **Storage:** Minimum **1GB free space** for recovered files  
- **Python Version:** **Python 3.8+**  

## **📦 Install Required Libraries**
Before using the tool, install the required Python packages:  
```sh
pip install pyqt6 psutil tqdm
```

## **🛠️ Running the Tool**
1️⃣ **Download the script** and save it as `file_recovery.py`.  
2️⃣ Open **Command Prompt (CMD)** or **Terminal** and navigate to the script’s location.  
3️⃣ Run the program:  
```sh
python file_recovery.py
```

---

# **4️⃣ How to Use the Tool (Step-by-Step Guide)**  

## **1️⃣ Open the Application**
- **Run `file_recovery.py`**
- The program **checks for Admin Privileges** (this ensures full disk access).  
- If **no admin privileges**, the tool **disables recovery functions** (for security reasons).  

---

## **2️⃣ Select the Drive to Scan**
- Use the **dropdown menu** to select a disk (`C:`, `D:`, `E:` etc.).  
- This tells the program **which drive to scan** for deleted files.  

---

## **3️⃣ Start Scanning**
- Click the **"Scan for Deleted Files"** button.  
- The tool will **search raw disk sectors** for lost files based on **file signatures** (JPG, PNG, DOCX, etc.).  
- A **progress bar** will update as the scan progresses.  

✅ **Scanning time depends on the drive size** (it may take a few minutes).  

---

## **4️⃣ View Deleted Files**
- Once scanning is complete, the **deleted files** will appear in the list.  
- Each entry shows **File Type & Sector** where it was found.  

🔹 **Example Output:**  
```
✅ JPG found at sector 1521034
✅ PDF found at sector 3210410
✅ MP4 found at sector 6102341
```

---

## **5️⃣ Recover a Deleted File**
1. Select the **file you want to recover** from the list.  
2. Click **"Recover Selected File"**.  
3. A **dialog box** will ask where to save the recovered file.  
4. Choose a **recovery folder** (preferably on another drive to avoid overwriting).  
5. Click **OK**, and the file will be restored!  

---

# **5️⃣ File Recovery Process Explained**
### **How the Tool Finds Files**
- The tool scans for **unique file headers** (signatures) of different file formats.
- When a match is found, the tool **extracts the file** starting from that sector.
- The file is **saved as a new file** in the recovery folder.

### **Supported File Types & Their Signatures**
| File Type | Signature |
|-----------|-----------|
| JPG | `FF D8 FF` |
| PNG | `89 50 4E 47` |
| PDF | `%PDF` |
| DOCX/XLSX/PPTX | `PK 03 04` |
| MP4 | `00 00 00 18 66 74 79 70 6D 70 34` |
| ZIP | `PK 03 04` |
| RAR | `52 61 72 21` |
| EXE | `4D 5A` |
| MP3 | `49 44 33` |
| TXT (UTF-8) | `EF BB BF` |

---

# **6️⃣ Safety Tips & Best Practices**
⚠️ **Recover files ASAP before they are overwritten!**  
⚠️ **Never recover files to the same drive you’re scanning!**  
⚠️ **Avoid using SSDs if possible** (TRIM erases deleted files permanently).  
⚠️ **Ensure you have enough storage** for recovered files.  

✅ **Recommended:**  
✔️ Use an **external drive** to save recovered files.  
✔️ Stop using the drive **immediately after deletion** (to prevent overwriting).  
✔️ If a file **isn't fully recovered**, try scanning again **before saving new data**.  

---

# **7️⃣ FAQs & Troubleshooting**

### **Q: Why can’t I recover some files?**
❌ Some files may be **overwritten** by new data and are **unrecoverable**.  

### **Q: Why is the recovered file corrupted?**
🔹 The file might be **partially overwritten**, leading to missing data.  
🔹 Some **files require metadata** (e.g., DOCX, MP4), which may be lost.  

### **Q: The tool doesn’t detect my external drive!**
🔹 Ensure the external drive is **connected properly** and **formatted correctly (NTFS/FAT)**.  
🔹 Restart the tool and **try scanning again**.  

### **Q: Why does scanning take a long time?**
🔹 Larger drives **take longer to scan**. The tool **reads every sector** for lost files.  

### **Q: Can I use this on a USB or SD card?**
✅ Yes! As long as the USB/SD **has not been formatted with TRIM**. 