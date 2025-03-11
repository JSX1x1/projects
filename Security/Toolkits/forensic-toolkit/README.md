# Forensic & Cybersecurity Toolkit  

This repository contains a suite of **ethical forensic and cybersecurity tools** designed for **digital investigators, cybersecurity professionals, ethical hackers, and researchers**. These tools help with **file forensics, cryptographic analysis, steganography detection, and digital security assessments**.  

🚨 **Disclaimer:** These tools are provided strictly for **legal and ethical cybersecurity research**. **Misuse for illegal purposes is strictly prohibited**. The developer assumes **no responsibility for any misuse**.  

---

## 📌 Features  

✅ **Forensic file analysis** – Extract metadata, hashes, and hex dumps  
✅ **Hex dump investigation** – Detect file type, analyze entropy, and view byte frequency  
✅ **Hash identification & verification** – Recognize hash types and validate integrity  
✅ **MD5 hash resolution (ethical)** – Compare MD5 hashes with common values and user-provided dictionaries  
✅ **Password generation & hashing** – Secure password creation and multi-algorithm hashing  
✅ **Steganography detection & extraction** – Identify hidden messages in images with LSB analysis  
✅ **File signature identification** – Detect true file type using magic bytes and flag mismatched extensions  

**All tools run 100% client-side** for privacy and security.  

---

## 🚀 Installation & Usage  

These tools **require no installation** and can be run directly in a web browser.  

### **🔹 Option 1: Run Locally**  
1. **Clone or download the repository:**  
   ```sh
   git clone https://github.com/JSX1x1/forensic-toolkit.git
   ```
2. **Open any `.html` file** in a web browser (Chrome, Firefox, Edge, etc.).  
3. **Use the tools responsibly** for cybersecurity research.  

### **🔹 Option 2: Host Online (GitHub Pages)**  
1. Go to your **GitHub repository settings**.  
2. Enable **GitHub Pages** under the **Pages section**.  
3. Access the tools at:  
   ```
   https://JSX1x1.github.io/forensic-toolkit/
   ```

---

## 🔍 **Tool Descriptions & How to Use**  

### 1️⃣ **Forensic Analysis Tool**  
**Description:** Extracts metadata, generates hash values (MD5, SHA-256), and provides a hex dump preview of uploaded files.  

**How to Use:**  
- Upload a file to analyze its properties.  
- View its **hex dump** and **calculate hash values**.  
- Detect **potential tampering or corruption**.  

**Use Case:** Useful for verifying **file integrity**, **detecting altered files**, and **analyzing unknown file formats**.  

**Safety Hint:** Avoid running untrusted files, as they may contain malware.  

---

### 2️⃣ **Hex Dump Analyzer**  
**Description:** Analyzes raw hexadecimal data, detects file types, converts hex to ASCII, and performs entropy analysis.  

**How to Use:**  
- Paste a **hex dump** into the input field.  
- View its **decoded ASCII representation**.  
- Analyze **entropy** to determine if the data is encrypted or compressed.  

**Use Case:** Helps forensic analysts **decode unknown file structures** and **identify encrypted content**.  

**Safety Hint:** Higher entropy values often indicate **compressed or encrypted data**.  

---

### 3️⃣ **Hash Analyzer**  
**Description:** Identifies hash algorithms based on length and format, verifies hashes, and checks for known vulnerabilities.  

**How to Use:**  
- Enter a **hash value** to determine its algorithm (MD5, SHA-1, SHA-256, etc.).  
- Compare a **hash with user-input data** for integrity verification.  
- Review **security risks** associated with weak hashing algorithms.  

**Use Case:** Helps in **file verification, password security assessments, and cryptographic analysis**.  

**Safety Hint:** Avoid using **MD5 and SHA-1** for security applications, as they are vulnerable to attacks.  

---

### 4️⃣ **MD5 Hash Resolver (Ethical)**  
**Description:** Matches an MD5 hash against common hash values and user-provided wordlists, without using brute-force techniques.  

**How to Use:**  
- Enter an **MD5 hash** and check for a match in **common passwords**.  
- Upload a **custom dictionary file** for additional testing.  

**Use Case:** Helps verify if a password or data string corresponds to a **known weak MD5 hash**.  

**Safety Hint:** This tool **does not use brute-force or illegal cracking methods** and should only be used for research purposes.  

---

### 5️⃣ **Password Creator & Hasher**  
**Description:** Generates secure passwords and hashes them using MD5, SHA-1, SHA-256, and SHA-512.  

**How to Use:**  
- Specify **password length** and choose **complexity options**.  
- Generate a **random secure password**.  
- Hash passwords using various algorithms.  

**Use Case:** Helps **create strong, unique passwords** and evaluate **different hashing techniques**.  

**Safety Hint:** Always store passwords using **secure hashing algorithms** like **bcrypt or Argon2**.  

---

### 6️⃣ **Steganography Tool**  
**Description:** Hides and extracts messages in images using **LSB (Least Significant Bit) steganography** and **entropy analysis**.  

**How to Use:**  
- Upload an **image** and enter a **hidden message** to embed it.  
- Extract a **hidden message** from a stego-image.  
- Perform **entropy analysis** and **LSB detection** to identify modified pixels.  

**Use Case:** Useful for **detecting hidden communication in images** and **steganography research**.  

**Safety Hint:** Steganography can be **misused for data exfiltration**—use responsibly.  

---

### 7️⃣ **File Signature Identifier**  
**Description:** Identifies the true file type using **magic numbers (file headers)** and warns about **mismatched extensions**.  

**How to Use:**  
- Upload a file to analyze its **magic byte signature**.  
- View the **first 32 bytes in hex** for forensic examination.  
- Compare the detected file type against the **declared file extension**.  

**Use Case:** Helps **detect renamed malicious files** (e.g., `malware.exe` disguised as `image.jpg`).  

**Safety Hint:** Always verify unknown files before opening them to avoid malware infections.  

---

## ⚠ **Security & Ethical Guidelines**  

✔ **Use these tools responsibly** – They are intended for **forensic research, cybersecurity education, and ethical hacking**.  

✔ **Do not use these tools for unauthorized activities** – Using them for illegal hacking or privacy invasion is **strictly prohibited**.  

✔ **No brute-force attacks** – These tools do **not** perform brute-force attacks or password cracking beyond legal security testing.  

✔ **Stay within legal boundaries** – If using these tools for security testing, ensure you have **explicit permission** from the system owner.  

---

## 📜 License  
This project is licensed under the **MIT License** – You are free to use and modify it for ethical research purposes.  

---

## 🛠 Contributing  
Contributions to improve this toolkit are welcome! Please ensure all additions comply with **ethical cybersecurity guidelines**.  

---

## 📬 Contact  
For questions, issues, or contributions, feel free to create an **issue** or **pull request** in the repository.  

---

🔹 **Maintained by:** `JSX1x1`  
🔹 **GitHub Repository:** [Forensic & Cybersecurity Toolkit](https://github.com/JSX1x1/forensic-toolkit) 