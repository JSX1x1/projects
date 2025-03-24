using System;
using System.IO;

namespace ConsoleCLI
{
    class Program
    {
        // Dark mode colors
        static ConsoleColor backgroundColor = ConsoleColor.Black;
        static ConsoleColor textColor = ConsoleColor.White;

        static void Main(string[] args)
        {
            // Set the console to dark mode
            ApplyDarkMode();

            // Greet user
            Console.WriteLine("Welcome to the Advanced Console CLI!");
            Console.WriteLine("Type 'help' to see available commands.");
            Console.WriteLine("All commands are case-insensitive.");

            // Main loop for processing commands
            while (true)
            {
                Console.Write("\n> ");
                string input = Console.ReadLine()?.Trim().ToLower();

                if (input == "exit")
                {
                    Exit();
                }
                else if (input == "help")
                {
                    DisplayHelp();
                }
                else if (input.StartsWith("create file "))
                {
                    CreateFile(input.Substring(12));
                }
                else if (input.StartsWith("delete file "))
                {
                    DeleteFile(input.Substring(12));
                }
                else if (input.StartsWith("create dir "))
                {
                    CreateDirectory(input.Substring(11));
                }
                else if (input == "list files")
                {
                    ListFiles();
                }
                else if (input.StartsWith("show file "))
                {
                    ShowFileContent(input.Substring(10));
                }
                else
                {
                    Console.WriteLine("Unknown command. Type 'help' for help.");
                }
            }
        }

        static void ApplyDarkMode()
        {
            Console.BackgroundColor = backgroundColor;
            Console.ForegroundColor = textColor;
            Console.Clear(); // Refresh console to apply dark mode
        }

        static void DisplayHelp()
        {
            Console.WriteLine("\nAvailable Commands:");
            Console.WriteLine("  help             - Show available commands");
            Console.WriteLine("  exit             - Exit the application");
            Console.WriteLine("  create file [name]  - Create a new file with the given name");
            Console.WriteLine("  delete file [name]  - Delete the specified file");
            Console.WriteLine("  create dir [name]   - Create a new directory with the specified name");
            Console.WriteLine("  list files        - List all files in the current directory");
            Console.WriteLine("  show file [name]   - Show content of the specified file");
        }

        static void CreateFile(string fileName)
        {
            if (string.IsNullOrWhiteSpace(fileName))
            {
                Console.WriteLine("Error: Invalid file name.");
                return;
            }

            Console.WriteLine($"Enter content for file '{fileName}' (Press Ctrl+Z to finish):");

            try
            {
                string content = Console.ReadLine();
                if (string.IsNullOrWhiteSpace(content))
                {
                    Console.WriteLine("Error: File content cannot be empty.");
                    return;
                }

                // Create the file and write content
                File.WriteAllText(fileName, content);
                Console.WriteLine($"File '{fileName}' created successfully.");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error creating file: {ex.Message}");
            }
        }

        static void DeleteFile(string fileName)
        {
            if (string.IsNullOrWhiteSpace(fileName))
            {
                Console.WriteLine("Error: Invalid file name.");
                return;
            }

            try
            {
                if (File.Exists(fileName))
                {
                    File.Delete(fileName);
                    Console.WriteLine($"File '{fileName}' deleted successfully.");
                }
                else
                {
                    Console.WriteLine($"Error: File '{fileName}' not found.");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error deleting file: {ex.Message}");
            }
        }

        static void CreateDirectory(string dirName)
        {
            if (string.IsNullOrWhiteSpace(dirName))
            {
                Console.WriteLine("Error: Invalid directory name.");
                return;
            }

            try
            {
                if (Directory.Exists(dirName))
                {
                    Console.WriteLine($"Error: Directory '{dirName}' already exists.");
                }
                else
                {
                    Directory.CreateDirectory(dirName);
                    Console.WriteLine($"Directory '{dirName}' created successfully.");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error creating directory: {ex.Message}");
            }
        }

        static void ListFiles()
        {
            try
            {
                string[] files = Directory.GetFiles(Directory.GetCurrentDirectory());

                if (files.Length == 0)
                {
                    Console.WriteLine("No files found in the current directory.");
                }
                else
                {
                    Console.WriteLine("\nFiles in the current directory:");
                    foreach (string file in files)
                    {
                        Console.WriteLine($"- {Path.GetFileName(file)}");
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error listing files: {ex.Message}");
            }
        }

        static void ShowFileContent(string fileName)
        {
            if (string.IsNullOrWhiteSpace(fileName))
            {
                Console.WriteLine("Error: Invalid file name.");
                return;
            }

            try
            {
                if (File.Exists(fileName))
                {
                    string content = File.ReadAllText(fileName);
                    Console.WriteLine($"\nContent of '{fileName}':\n");
                    Console.WriteLine(content);
                }
                else
                {
                    Console.WriteLine($"Error: File '{fileName}' not found.");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error reading file: {ex.Message}");
            }
        }

        static void Exit()
        {
            Console.WriteLine("Exiting the application...");
            Environment.Exit(0);
        }
    }
}
