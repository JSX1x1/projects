## Brute Force Emulator – Educational Simulation  
*A PyQt6-based GUI to visualize how brute-force attacks work*  

### 🚀 **Overview**  
This project is an **educational tool** designed to **simulate** how brute-force attacks work in password cracking. It does **not** perform actual attacks on any real systems or networks. Instead, it visually represents the process using **PyQt6** to help cybersecurity enthusiasts, students, and researchers understand brute-force mechanics.  

---

## 📜 **How It Works**  
### 🎯 **Concept**  
Brute-force attacks involve **systematically guessing** a password until the correct one is found. This program demonstrates this **without targeting any real accounts**.  

### 🖥 **How the Code Works**  

1. **User sets a password** (which the emulator will attempt to "crack").  
2. **The emulator starts guessing** using a **dictionary-based** or **incremental** approach.  
3. **Each guess is displayed in real-time** inside a PyQt6 GUI.  
4. **When the correct password is found**, the program stops and displays success.  

### 🔍 **Code Breakdown**  

```python
# Brute force function (simulates guessing passwords)
def brute_force_attack(target_password, char_set, max_length):
    for length in range(1, max_length + 1):
        for guess in itertools.product(char_set, repeat=length):
            guessed_password = ''.join(guess)
            update_gui_with_attempt(guessed_password)  # Show attempt in the UI
            if guessed_password == target_password:
                return guessed_password  # Password found!
```
- **`itertools.product`** generates all possible combinations.  
- **`update_gui_with_attempt(guessed_password)`** updates the GUI with each guess.  
- **Stops when the correct password is found.**  

---

## 📖 **How to Use**  
### 🔧 **Installation & Setup**  

#### **Step 1: Install Python**  
Ensure you have Python **3.8+** installed. If not, download it from [python.org](https://www.python.org/).  

#### **Step 2: Install Dependencies**  
Run the following command to install **PyQt6** and other required libraries:  
```sh
pip install PyQt6
```

#### **Step 3: Run the Emulator**  
Download the script and run:  
```sh
python brute_force_emulator.py
```

---

## 🎯 **What Is This For?**  
- **Cybersecurity Education** – Learn how brute-force attacks function.  
- **Visual Demonstration** – Shows the attack process **without harming real systems**.  
- **Ethical Hacking Practice** – Helps in understanding the importance of **strong passwords** and defense mechanisms.  

⚠️ **This tool is NOT for hacking real accounts!**  

---

## ⚠️ **DISCLAIMER**  
> This program is **strictly for educational purposes**.  
> Do **NOT** use it to attack real websites, networks, or personal accounts.  
> Unauthorized use of brute-force attacks **is illegal** and may result in **severe legal consequences**.  
> The developer is **not responsible** for any misuse.  

Use this responsibly and **always follow ethical hacking guidelines**.  

---

## 🛡 **Stay Safe & Ethical!**  
This project is meant to educate and spread **awareness** about cybersecurity risks. Use it wisely, and always prioritize **ethical hacking practices**.