# **Document Management System (PyQt6)**  
This is a **modern, dark-themed Document Management System (DMS)** built with **Python & PyQt6**.  
It allows users to:  
✅ **Create & Manage Folders**  
✅ **Create & Edit Documents (`.xdoc` format)**  
✅ **Track Document Versions**  
✅ **Assign Documents** to contacts with reasons  
✅ **Save and Restore Document Changes**  

## **Features**  
- **Dark Mode UI:** Modern and intuitive design  
- **Tab-Based Navigation:**  
  -**Create** (New Document & Folder)  
  -**Edit Document** (Text Editor with Save & Highlighting)  
  -**Assignments** (Assign documents to contacts)  
  -**Version History Panel** (View & restore previous versions)  
- **Automatic Versioning:** Each document keeps a full history of changes  
- **Real-Time Change Highlighting:** Unsaved changes are visually marked  
- **Easy Navigation:** File tree panel to browse folders & documents  

---

## 📦 **Installation**  
### **1. Install Python (if not installed)**  
Ensure you have Python **3.10+** installed. You can check with:  
```sh
python --version
```
If not installed, download it from [python.org](https://www.python.org/).  

### **2. Install Required Packages**  
This project uses **PyQt6** for the GUI. Install it with:  
```sh
pip install PyQt6
```

---

## 🛠 **How to Use**  
### **1️⃣ Run the Application**  
After installing the dependencies, run the program with:  
```sh
python document_manager.py
```

### **2️⃣ Create a New Folder**  
1. Open the **"Create" tab**  
2. Click **"New Folder"**  
3. Choose a location to create a new folder  

### **3️⃣ Create a New Document**  
1. Open the **"Create" tab**  
2. Click **"New Document"**  
3. Choose a location and enter a filename (`example.xdoc`)  

### **4️⃣ Edit an Existing Document**  
1. Navigate to the file tree panel  
2. Select a `.xdoc` document to open it  
3. Edit the document in the **"Edit Document"** tab  
4. Click **"Save Changes"** to save  

### **5️⃣ View & Restore Versions**  
1. Open a document  
2. Look at the **Version History** panel (on the right)  
3. Click a previous version to view it  
4. Manually copy/paste if you want to restore  

### **6️⃣ Assign a Document**  
1. Go to the **"Assignments"** tab  
2. Enter a **Contact Name** & **Reason**  
3. Click **"Assign"**  
4. The assignment is stored inside the `.xdoc` file  

---

## 🔍 **How Document Storage Works**  
All documents are saved as **`.xdoc` files** (JSON format).  

### **Example `.xdoc` File:**
```json
{
    "document_name": "example",
    "versions": [
        {
            "timestamp": "2025-03-14T12:00:00",
            "content": "Initial content"
        },
        {
            "timestamp": "2025-03-14T12:30:00",
            "content": "Edited content"
        }
    ],
    "assignments": [
        {
            "contact": "John Doe",
            "reason": "Review"
        }
    ]
}
```
✅ **Each document saves its own version history**  
✅ **Assignments are stored inside the document**  

---

## ❓ **Troubleshooting**  
### **App Doesn't Start?**  
Run the script in the terminal and check for errors:  
```sh
python document_manager.py
```
Make sure **PyQt6** is installed. If not, install it:  
```sh
pip install PyQt6
```

### **File Not Saving?**  
Ensure you **click "Save Changes"** after editing a document.  

### **Can’t Find a File?**  
Check the **file tree panel** and make sure the correct directory is loaded.  

---

## 🎯 **Future Improvements**  
- **Document Search Feature**  
- **Multi-User Support**  
- **Cloud Storage Integration**  

---

## 📝 **Author**  
**Developed by:** _[JSX_1x1]_  
**GitHub:** _[[My Profile](https://github.com/JSX1x1)]_  
