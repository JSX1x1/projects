# **URL Scanner & Security Checker - User Manual**  

### **🔹 Overview**  
The **URL Scanner & Security Checker** is a tool that helps detect **malicious websites** using a **local blacklist** and **VirusTotal API**.  

✅ **Detects phishing, malware, and unsafe websites**  
✅ **GUI (User-Friendly) & CLI (Fast & Lightweight) versions**  
✅ **Works on Windows, macOS, and Linux**  
✅ **No login or complex setup required**  

---

# **📂 1. GUI Version (`url_scanner_GUI.py`)**  

### **📌 Features**  
✔ **User-friendly interface** with URL input & scan results  
✔ **Checks URLs against VirusTotal API** (if API key is provided)  
✔ **Works offline using a built-in local blacklist**  

### **📥 Installation & Setup**  
1️⃣ **Install Python & dependencies**  
   ```sh
   pip install PyQt6 requests
   ```
2️⃣ **(Optional) Set your VirusTotal API Key** in `url_scanner_GUI.py`:  
   ```python
   API_KEY = "YOUR_VIRUSTOTAL_API_KEY"
   ```
   *(Get a free API key at [VirusTotal](https://www.virustotal.com/))*  

---

### **🚀 Running the GUI Scanner**  
```sh
python url_scanner_GUI.py
```
#### **🖥️ Steps to Use**
1. **Enter a URL** in the input field  
2. Click **"Scan URL"**  
3. The tool will check the URL:  
   - ✅ **Safe:** No threats found  
   - 🚨 **Malicious:** Detected in VirusTotal or local blacklist  

---

## **⌨️ 2. CLI Version (`url_scanner_CLI.cpp`)**  

### **📌 Features**  
✔ **Fast command-line URL scanner**  
✔ **Checks URLs against a local blacklist**  
✔ **Uses VirusTotal API for real-time scanning**  

### **📥 Installation & Setup**  
1️⃣ **Install required libraries**  
   - **Linux/macOS:**  
     ```sh
     sudo apt install libcurl4-openssl-dev libjsoncpp-dev
     ```
   - **Windows (MinGW):**  
     ```sh
     pacman -S mingw-w64-x86_64-curl mingw-w64-x86_64-jsoncpp
     ```
2️⃣ **(Optional) Set your VirusTotal API Key** in `url_scanner_CLI.cpp`:  
   ```cpp
   const string VIRUSTOTAL_API_KEY = "YOUR_VIRUSTOTAL_API_KEY";
   ```

---

### **🚀 Compiling & Running the CLI Scanner**  
#### **1️⃣ Compile the program**  
```sh
g++ url_scanner_CLI.cpp -o url_scanner -lcurl -ljsoncpp
```
#### **2️⃣ Run the scanner**  
```sh
./url_scanner https://example.com
```
#### **3️⃣ Scan results will show:**  
- ✅ **Safe:** No threats detected  
- 🚨 **Malicious:** Flagged in local blacklist or VirusTotal  

---

# **📊 Example Usage & Output**  

### **🔎 Safe URL**
```sh
./url_scanner https://example.com
```
```
Scanning URL: https://example.com...
Not found in local blacklist. Checking VirusTotal...
No known threats detected by VirusTotal.
```

### **⚠️ Malicious URL**
```sh
./url_scanner https://badwebsite.com
```
```
Scanning URL: https://badwebsite.com...
WARNING! This URL is flagged as MALICIOUS in local blacklist!
```
OR
```
Scanning URL: https://badwebsite.com...
Not found in local blacklist. Checking VirusTotal...
WARNING! This URL is flagged as MALICIOUS by VirusTotal!
```

---

# **📌 Notes**
- **VirusTotal API usage is optional** but recommended for real-time threat detection.  
- The **local blacklist** allows **offline scanning** without an internet connection.  
- The **CLI version is faster** for bulk URL scanning, while the **GUI version is more user-friendly**.  