using System;
using System.IO;
using System.Runtime.InteropServices;
using System.Reflection;
using System.Threading;

namespace RealWorldLibrary
{
    public class Utility
    {
        private static readonly string logFilePath = Path.Combine(Path.GetDirectoryName(Assembly.GetExecutingAssembly().Location), "library.log");
        private static readonly object lockObj = new object();

        // Logs messages to a file
        private static void LogMessage(string message)
        {
            lock (lockObj)
            {
                try
                {
                    File.AppendAllText(logFilePath, $"{DateTime.Now}: {message}\n");
                }
                catch (Exception ex)
                {
                    Console.WriteLine("Logging failed: " + ex.Message);
                }
            }
        }

        // Public method: Adds two numbers
        public int Add(int a, int b)
        {
            try
            {
                int result = a + b;
                LogMessage($"Add({a}, {b}) = {result}");
                return result;
            }
            catch (Exception ex)
            {
                LogMessage($"Error in Add: {ex.Message}");
                throw;
            }
        }

        // Public method: Reads a text file (Thread-Safe)
        public string ReadFile(string filePath)
        {
            try
            {
                lock (lockObj)
                {
                    if (!File.Exists(filePath))
                        throw new FileNotFoundException("File not found", filePath);

                    string content = File.ReadAllText(filePath);
                    LogMessage($"ReadFile({filePath}) - Success");
                    return content;
                }
            }
            catch (Exception ex)
            {
                LogMessage($"Error in ReadFile: {ex.Message}");
                throw;
            }
        }

        // Public method: Gets current system time
        public string GetSystemTime()
        {
            string time = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");
            LogMessage($"GetSystemTime() = {time}");
            return time;
        }
    }

    public static class NativeExports
    {
        // Exports a native function for C/C++ or other interop use
        [DllExport("MultiplyNumbers", CallingConvention = CallingConvention.StdCall)]
        public static int MultiplyNumbers(int a, int b)
        {
            int result = a * b;
            Utility utility = new Utility();
            utility.LogMessage($"MultiplyNumbers({a}, {b}) = {result}");
            return result;
        }

        // Returns the current system time as a C-compatible string
        [DllExport("GetSystemTime", CallingConvention = CallingConvention.StdCall)]
        public static IntPtr GetSystemTime()
        {
            string time = DateTime.Now.ToString("yyyy-MM-dd HH:mm:ss");
            IntPtr ptr = Marshal.StringToHGlobalAnsi(time);
            return ptr;
        }
    }
}
