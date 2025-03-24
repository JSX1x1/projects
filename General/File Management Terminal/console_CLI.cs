using System;
using System.IO;
using System.Diagnostics;

class CommandLineTerminal
{
    static string currentDirectory = Directory.GetCurrentDirectory();

    static void Main(string[] args)
    {
        Console.Title = "C# Command Line Terminal";
        Console.BackgroundColor = ConsoleColor.Cyan;
        Console.ForegroundColor = ConsoleColor.Black;
        Console.Clear();

        Console.WriteLine("C# Command Line Terminal - Type 'help' for available commands.");

        while (true)
        {
            Console.Write($"[{currentDirectory}]> ");
            string input = Console.ReadLine();

            if (string.IsNullOrWhiteSpace(input))
                continue;

            string command = input.Split(' ')[0];
            string arguments = input.Length > command.Length ? input.Substring(command.Length).Trim() : string.Empty;

            switch (command.ToLower())
            {
                case "mkdir":
                    CreateDirectory(arguments);
                    break;
                case "rmdir":
                    RemoveDirectory(arguments);
                    break;
                case "touch":
                    CreateFile(arguments);
                    break;
                case "edit":
                    EditFile(arguments);
                    break;
                case "cd":
                    ChangeDirectory(arguments);
                    break;
                case "ls":
                    ListDirectory();
                    break;
                case "tree":
                    ShowTree();
                    break;
                case "help":
                    ShowHelp();
                    break;
                default:
                    RunSystemCommand(input);
                    break;
            }
        }
    }

    static void CreateDirectory(string path)
    {
        if (string.IsNullOrWhiteSpace(path))
        {
            Console.WriteLine("Error: Directory name not specified.");
            return;
        }

        try
        {
            Directory.CreateDirectory(path);
            Console.WriteLine($"Directory '{path}' created.");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error creating directory: {ex.Message}");
        }
    }

    static void RemoveDirectory(string path)
    {
        if (string.IsNullOrWhiteSpace(path))
        {
            Console.WriteLine("Error: Directory name not specified.");
            return;
        }

        try
        {
            Directory.Delete(path);
            Console.WriteLine($"Directory '{path}' removed.");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error removing directory: {ex.Message}");
        }
    }

    static void CreateFile(string filename)
    {
        if (string.IsNullOrWhiteSpace(filename))
        {
            Console.WriteLine("Error: Filename not specified.");
            return;
        }

        try
        {
            using (File.Create(filename)) { }
            Console.WriteLine($"File '{filename}' created.");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error creating file: {ex.Message}");
        }
    }

    static void EditFile(string filename)
    {
        if (string.IsNullOrWhiteSpace(filename))
        {
            Console.WriteLine("Error: Filename not specified.");
            return;
        }

        try
        {
            // Open the file with the default editor (Notepad for Windows)
            Process.Start("notepad.exe", filename);
            Console.WriteLine($"Opening file '{filename}' for editing.");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error editing file: {ex.Message}");
        }
    }

    static void ChangeDirectory(string path)
    {
        if (string.IsNullOrWhiteSpace(path))
        {
            Console.WriteLine("Error: Directory path not specified.");
            return;
        }

        try
        {
            // Change the current directory
            Directory.SetCurrentDirectory(path);
            currentDirectory = Directory.GetCurrentDirectory();
            Console.WriteLine($"Changed directory to '{currentDirectory}'.");
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error changing directory: {ex.Message}");
        }
    }

    static void ListDirectory()
    {
        try
        {
            var files = Directory.GetFileSystemEntries(currentDirectory);
            if (files.Length == 0)
            {
                Console.WriteLine("The directory is empty.");
            }
            else
            {
                foreach (var file in files)
                {
                    Console.WriteLine(file);
                }
            }
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error listing directory: {ex.Message}");
        }
    }

    static void ShowTree()
    {
        try
        {
            // Run the 'tree' command if available on the system
            ProcessStartInfo psi = new ProcessStartInfo("tree", "/f /a")
            {
                RedirectStandardOutput = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };
            Process process = Process.Start(psi);
            process.WaitForExit();
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error displaying tree: {ex.Message}");
        }
    }

    static void ShowHelp()
    {
        string helpText = @"
        Supported commands:

        mkdir <directory>     - Create a new directory.
        rmdir <directory>     - Remove an existing directory.
        touch <filename>      - Create an empty file with the given filename.
        edit <filename>       - Open the specified file in the default editor (Notepad).
        cd <path>             - Change the current directory.
        ls                    - List the contents of the current directory.
        tree                  - Display the directory tree structure.
        help                  - Display this help message.
        ";

        Console.WriteLine(helpText);
    }

    static void RunSystemCommand(string input)
    {
        try
        {
            ProcessStartInfo psi = new ProcessStartInfo("cmd", $"/C {input}")
            {
                RedirectStandardOutput = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };
            Process process = Process.Start(psi);
            process.WaitForExit();
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Error executing command: {ex.Message}");
        }
    }
}
