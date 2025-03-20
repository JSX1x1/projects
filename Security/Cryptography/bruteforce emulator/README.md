# Brute Force Emulator – Educational Simulation  
*A PyQt6-based GUI & C# Console Simulation of Brute-Force Attacks*  

---

## 🚀 **Overview**  
This project is an **educational tool** designed to **simulate** how brute-force attacks work in password cracking. It does **not** perform actual attacks on any real systems or networks. Instead, it visually represents the process using **PyQt6 (GUI)** and **C# Console Application** to help cybersecurity enthusiasts, students, and researchers understand brute-force mechanics.  

> ⚠️ **This project is for learning purposes only. Misuse is strictly prohibited.**  
> NOTE: THIS PROGRAMM DOES NOT ACTUALLY ATTEMPT BRUTEFORCE

---

## 📜 **How It Works**  

### 🎯 **Concept**  
Brute-force attacks involve **systematically guessing** a password until the correct one is found. This program demonstrates this **without targeting any real accounts**.  

- **PyQt6 Version (GUI)**: Provides a **visual representation** of brute-force attempts.  
- **C# Console Version**: Simulates the attack process in a **text-based format**.  

Both versions work by:  
1. **User setting a target password**.  
2. **The emulator simulating password guessing**.  
3. **Each guess being displayed in real-time**.  
4. **Stopping when the correct password is found**.  

---

## 💻 **Code Explanations**  

### 🖥 **Python (PyQt6 GUI Version)**  

#### 🔍 **Brute Force Attack Logic**  
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
- **`itertools.product`** generates all possible password combinations.  
- **`update_gui_with_attempt(guessed_password)`** updates the GUI in real-time.  
- **Stops when the correct password is found**.  

---

### 🖥 **C# Console Version**  

#### 🔍 **Brute Force Attack Logic**  
```csharp
static string BruteForceAttack(string target, string charSet, int maxLength)
{
    foreach (int length in Enumerable.Range(1, maxLength))
    {
        foreach (var guess in GenerateCombinations(charSet, length))
        {
            Console.Write($"\rTrying: {guess}  "); // Update console with current guess
            Thread.Sleep(10); // Simulate realistic processing delay

            if (guess == target)
            {
                return guess; // Password matched!
            }
        }
    }
    return null;
}
```
- **Uses recursive combinations** to generate password guesses.  
- **Simulates real-time brute-force attacks in the console**.  
- **Stops once the password is found**.  

---

## 📖 **How to Use**  

### 🔧 **Python (PyQt6 GUI Version)**  

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

### 🔧 **C# Console Version**  

#### **Step 1: Install .NET SDK**  
Ensure you have **.NET 6.0+** installed. Download it from [dotnet.microsoft.com](https://dotnet.microsoft.com/en-us/download).  

#### **Step 2: Compile & Run**  
1. Save the C# script as **`BruteForceEmulator.cs`**  
2. Open a terminal or command prompt and navigate to the file location.  
3. Compile the program:  
   ```sh
   dotnet build
   ```
4. Run the application:  
   ```sh
   dotnet run
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