## **File Compression Tool**  
*A simple yet powerful file compression and decompression tool with live size estimation and gain/loss ratio calculation.*

### **📂 Features**
✅ Supports **compression & decompression**  
✅ **Compression levels** (1-20 for fine control)  
✅ **Live file size calculation** before compression  
✅ **Gain/Loss ratio** to measure efficiency  
✅ **Color-coded results** for better visualization  
✅ Handles **empty files & errors gracefully**  

---

## **🖥️ GUI Version**
### **📌 How to Run**
1. **Install dependencies**  
   ```
   pip install PyQt6
   ```
2. **Run the GUI application**  
   ```
   python compressor_GUI.py
   ```
3. **Steps to Compress a File**  
   - Click **"Choose File"** and select the file you want to compress  
   - Adjust the **compression level slider (1-20)**  
   - Check the **live file size estimation**  
   - Click **"Compress File"** to compress  

4. **Steps to Decompress a File**  
   - Click **"Decompress File"**  
   - Select a **`.compressed`** file  
   - The file will be decompressed and saved as **`.decompressed`**  

---

## **🔧 CLI Version**
### **📌 How to Run**
1. **Run the CLI application**  
   ```
   python compressor_CLI.py --help
   ```
   *(Displays available commands and options.)*

2. **Compress a file**  
   ```
   python compressor_CLI.py compress myfile.txt -l 10
   ```
   - `compress` → Mode for compression  
   - `myfile.txt` → File to compress  
   - `-l 10` → Sets compression level (default is **5**)  

3. **Decompress a file**  
   ```
   python compressor_CLI.py decompress myfile.txt.compressed
   ```
   - `decompress` → Mode for decompression  
   - `myfile.txt.compressed` → File to decompress  

---

## **📊 Example Output (CLI)**
```
📊 Compression Details:
📏 Original Size: 1.25 MB
📦 Compressed Size: 512 KB
🔽 Reduction: 59.00%
📈 Gain/Loss Ratio: 2.44
✅ File compressed successfully: myfile.txt.compressed
```

```
📊 Decompression Details:
📦 Compressed Size: 512 KB
📏 Decompressed Size: 1.25 MB
📈 Gain/Loss Ratio: 2.44
✅ File decompressed successfully: myfile.txt.decompressed
```

---

## **📌 Notes**
- **Higher compression levels (15-20)** reduce file size **more** but take longer.  
- **Lower levels (1-5)** are **faster** but less efficient.  
- Works with **text, images, PDFs, and more!**  
- **Color-coded** output:  
  - 🟢 **Green** = Compression successful  
  - 🔴 **Red** = Compression inefficient  