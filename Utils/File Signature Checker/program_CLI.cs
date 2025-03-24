using System;
using System.Collections.Generic;
using System.IO;
using System.Security.Cryptography;
using System.Text;

namespace FileSignatureChecker
{
    class Program
    {
        // Dictionary of file signatures (Magic Numbers) and their corresponding file types.
        static Dictionary<byte[], string> fileSignatures = new Dictionary<byte[], string>(new ByteArrayComparer())
        {
            { new byte[] { 0x25, 0x50, 0x44, 0x46 }, "PDF" }, // PDF
            { new byte[] { 0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A }, "PNG" }, // PNG
            { new byte[] { 0xFF, 0xD8, 0xFF }, "JPEG" }, // JPEG
            { new byte[] { 0x50, 0x4B, 0x03, 0x04 }, "ZIP" }, // ZIP
            { new byte[] { 0x47, 0x49, 0x46, 0x38 }, "GIF" }, // GIF
            { new byte[] { 0x52, 0x61, 0x72, 0x21 }, "RAR" }, // RAR
            { new byte[] { 0xD0, 0xCF, 0x11, 0xE0, 0xA1, 0xB1, 0x1A, 0xE1 }, "DOC" }, // DOC (old Word)
            { new byte[] { 0x42, 0x4D }, "BMP" }, // BMP
            { new byte[] { 0x49, 0x44, 0x33 }, "MP3" }, // MP3 (ID3v2)
            { new byte[] { 0x52, 0x49, 0x46, 0x46 }, "AVI" }, // AVI
            { new byte[] { 0x1F, 0x8B, 0x08 }, "GZ" }, // GZ
            { new byte[] { 0x50, 0x4B, 0x03, 0x04 }, "DOCX" }, // DOCX (Office Open XML)
            { new byte[] { 0xFF, 0xFB }, "MP3" }, // MP3 (MPEG Audio)
            // Add more signatures here as needed...
        };

        static void Main(string[] args)
        {
            // Ask user to provide the file path
            Console.Write("Enter the full path of the file to check: ");
            string filePath = Console.ReadLine();

            // Validate file path
            if (!File.Exists(filePath))
            {
                Console.WriteLine("File does not exist. Please check the file path.");
                return;
            }

            // Read the file signature (first few bytes)
            byte[] fileBytes = ReadFileSignature(filePath);

            if (fileBytes != null)
            {
                // Check the file signature
                string fileType = CheckFileSignature(fileBytes);
                if (fileType != null)
                {
                    Console.WriteLine($"The file is of type: {fileType}");
                }
                else
                {
                    Console.WriteLine("The file signature does not match any known types.");
                }

                // Check the file integrity via hash comparison (SHA256)
                string fileHash = ComputeFileHash(filePath);
                Console.WriteLine($"SHA256 hash of the file: {fileHash}");

                // You can compare the computed hash with a known hash value for integrity checking.
                // Maybe add a dictionaries and add the hash values
            }
        }

        // Method to read the first few bytes of a file (signature)
        static byte[] ReadFileSignature(string filePath)
        {
            try
            {
                byte[] buffer = new byte[16]; // Buffer to hold the file signature (up to 16 bytes)
                using (FileStream fs = new FileStream(filePath, FileMode.Open, FileAccess.Read))
                {
                    fs.Read(buffer, 0, buffer.Length);
                }
                return buffer;
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error reading file: {ex.Message}");
                return null;
            }
        }

        // Method to check the file signature against known signatures
        static string CheckFileSignature(byte[] fileBytes)
        {
            foreach (var signature in fileSignatures)
            {
                if (StartsWith(fileBytes, signature.Key))
                {
                    return signature.Value;
                }
            }
            return null; // No match found
        }

        // Helper method to compare the beginning of a byte array with a known signature
        static bool StartsWith(byte[] fileBytes, byte[] signature)
        {
            for (int i = 0; i < signature.Length; i++)
            {
                if (fileBytes[i] != signature[i])
                {
                    return false;
                }
            }
            return true;
        }

        // Method to compute SHA256 hash of a file
        static string ComputeFileHash(string filePath)
        {
            using (SHA256 sha256 = SHA256.Create())
            {
                using (FileStream fs = new FileStream(filePath, FileMode.Open, FileAccess.Read))
                {
                    byte[] hashBytes = sha256.ComputeHash(fs);
                    StringBuilder hashStringBuilder = new StringBuilder();
                    foreach (byte b in hashBytes)
                    {
                        hashStringBuilder.Append(b.ToString("X2"));
                    }
                    return hashStringBuilder.ToString();
                }
            }
        }
    }

    // Custom comparer for byte arrays, needed for the Dictionary key comparison
    public class ByteArrayComparer : IEqualityComparer<byte[]>
    {
        public bool Equals(byte[] x, byte[] y)
        {
            if (x == null || y == null)
                return x == y;
            if (x.Length != y.Length)
                return false;
            for (int i = 0; i < x.Length; i++)
            {
                if (x[i] != y[i])
                    return false;
            }
            return true;
        }

        public int GetHashCode(byte[] obj)
        {
            int hash = 0;
            foreach (byte b in obj)
            {
                hash = (hash * 31) + b;
            }
            return hash;
        }
    }
}
