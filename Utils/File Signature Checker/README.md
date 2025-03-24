Certainly! Here's a detailed **README** for your **File Signature Checker** tool, including setup instructions, usage, features, and important considerations.

---

# **File Signature Checker**

## **Overview**

The **File Signature Checker** is a C# console application that allows you to:
- Identify file types based on their magic number (file signature).
- Verify the integrity of files using **SHA256** hashing, ensuring that the file has not been tampered with.
- Cross-check a file's computed hash against a known hash to detect any modifications or corruption.

The tool supports various file types, including multimedia files (images, audio, video), document files (PDF, DOCX), archives (ZIP, RAR), and more.

## **Features**
- **File Signature Detection**: Identify file types based on the first few bytes (magic numbers).
- **SHA256 Hashing**: Compute the hash of a file and verify its integrity.
- **Integrity Verification**: Compare the computed hash with a trusted known hash to check for file tampering.
- **Wide File Type Support**: Supports a broad range of file types (images, documents, audio, video, archives, executables).
- **Cross-check Extension**: Although not implemented here, extension verification can be added to avoid spoofing.

## **System Requirements**
- **.NET Core / .NET Framework**: The application is built in C#, and it is compatible with **.NET Core** and **.NET Framework**. .NET 6.0 or later is recommended for optimal performance.
- **Operating System**: Windows, Linux, or macOS (for the .NET Core version).

## **Setup and Installation**

### 1. **Clone the Repository**
First, clone the repository containing the code to your local machine:
```bash
git clone https://github.com/JSX1x1/projects/Utils/File Signature Checker.git
cd FileSignatureChecker
```

### 2. **Build the Project**
To build the project, follow these steps:

#### **Using Visual Studio**:
- Open the solution file `FileSignatureChecker.sln` in **Visual Studio**.
- Build the project using **Build > Build Solution**.

#### **Using .NET CLI**:
1. Open a terminal/command prompt in the project directory.
2. Run the following command to restore dependencies:
   ```bash
   dotnet restore
   ```
3. Build the project:
   ```bash
   dotnet build
   ```
4. Run the application:
   ```bash
   dotnet run
   ```

### 3. **Download Known Hashes**
You will need to manually obtain known hashes (SHA256) for the files you want to check for integrity. These known hashes can be sourced from trusted websites or other authenticated sources.

## **Usage**

### **Running the Application**
To run the program, follow the instructions below:

1. **Launch the Console Application**:
   - Open the terminal or command prompt and navigate to the directory where the application is located.
   - Run the following command:
     ```bash
     dotnet run
     ```

2. **Input the File Path**:
   When prompted, enter the full path of the file you want to check. For example:
   ```plaintext
   Enter the full path of the file to check: C:\Users\YourName\Downloads\example.pdf
   ```

3. **Output**:
   The program will display the following information:
   - **File Type**: Identifies the file type based on its magic number (e.g., PDF, PNG, DOCX, etc.).
   - **SHA256 Hash**: Displays the SHA256 hash of the file.
   - **Integrity Check**: Compares the computed hash with a known hash (provided by you) and notifies you whether the file has been tampered with.

Example output:
```plaintext
Enter the full path of the file to check: C:\Users\YourName\Downloads\example.pdf
The file is of type: PDF
SHA256 hash of the file: A3B0D8F4D9C4F9AB67F5EC9FAD9B4D4214B9F9A3D9829E9028C1B11A2D4A39B3
The file integrity is verified. The file has not been tampered with.
```

If the hash doesn't match the known hash:
```plaintext
Warning: The file integrity has been compromised! The file's hash does not match the expected hash.
```

### **Known Hash Comparison**:
To compare the computed hash with a known hash, replace the `knownHash` variable in the code with the actual hash value from a trusted source.

Example of a known hash comparison (in the code):
```csharp
string knownHash = "A3B0D8F4D9C4F9AB67F5EC9FAD9B4D4214B9F9A3D9829E9028C1B11A2D4A39B3";
```

### **File Signature Detection**:
The program detects the file type based on **magic numbers** (the first few bytes of the file). The `CheckFileSignature` method compares the file's first bytes with known signatures to determine the file type. It supports file types like PDF, PNG, JPEG, DOCX, and more.

#### **Example Supported File Types**:
- **PDF**: `%PDF` signature
- **PNG**: `89504E47` signature
- **JPEG**: `FFD8FF` signature
- **MP3**: `494433` signature
- **ZIP**: `504B0304` signature
- **GIF**: `47494638` signature
- **RAR**: `52617221` signature

You can extend the list by adding more signatures for different file types in the dictionary.

### **File Integrity Verification**:
The tool computes the **SHA256 hash** of the file and compares it with a known hash. This allows you to verify whether the file has been tampered with or corrupted. If the hash of the file matches the known hash, the file is verified as being intact. If not, the program will warn you about possible file manipulation.

## **Advanced Features**

- **Multiple Signature Support**: The application supports detection of multiple file types based on known file signatures (magic numbers). You can add more signatures to the dictionary to expand support for other file formats.
  
- **Cross-checking Extensions (Future Feature)**: To avoid **extension spoofing** (i.e., files with misleading extensions), you can implement an extension verification feature that checks whether the file extension matches its signature.

## **Security Considerations**
- **File Integrity**: Hashing ensures that the file has not been tampered with during download or transfer. Always compare the computed hash with a trusted hash provided by a source.
  
- **Extension Spoofing**: This tool only checks the file signature based on the magic numbers. While the signature-based method is reliable, you should also cross-check file extensions to prevent spoofing (e.g., a `.jpg` file could have the signature of a `.pdf` file).

- **Malware**: This tool only verifies the integrity of the file using hashes. It doesn’t scan for malware or other malicious content. For virus/malware detection, use an antivirus program.

## **Potential Improvements**
- **Cross-platform Extension Verification**: Implement additional checks to verify that a file’s extension matches its signature, preventing extension spoofing.
  
- **Signature Database**: Build a more extensive database of file signatures, including support for proprietary file types and formats not covered in the default dictionary.

- **Support for More Hashing Algorithms**: Implement more cryptographic hashing algorithms like SHA512, MD5, etc., for different levels of file verification.

- **GUI Version**: Develop a graphical user interface (GUI) for non-technical users who prefer a more visual method of interacting with the tool.

## **Known Issues**
- The tool currently relies on **manual entry** of known hashes. It would be helpful to automate this process by fetching hashes from a trusted database.
- The tool doesn’t currently perform file content analysis (e.g., malware detection) and should not be used as a replacement for antivirus software.