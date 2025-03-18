// SYSTEMUTIL.DLL
// This dll provides simple to use system management utilities for general usage.

using System;
using System.Diagnostics;
using System.IO;
using System.Net;
using System.Net.NetworkInformation;
using System.Runtime.InteropServices;
using System.Text;

namespace SystemUtilities
{
    public class SystemInfo
    {
        // Get Operating System Version
        public static string GetOSVersion()
        {
            return Environment.OSVersion.ToString();
        }

        // Get System Architecture (32-bit / 64-bit)
        public static string GetSystemArchitecture()
        {
            return Environment.Is64BitOperatingSystem ? "64-bit" : "32-bit";
        }

        // Get CPU Usage (%)
        public static float GetCPUUsage()
        {
            using (PerformanceCounter cpuCounter = new PerformanceCounter("Processor", "% Processor Time", "_Total"))
            {
                cpuCounter.NextValue();
                System.Threading.Thread.Sleep(500); // Allow counter to refresh
                return cpuCounter.NextValue();
            }
        }

        // Get Available RAM (MB)
        public static long GetAvailableMemory()
        {
            using (PerformanceCounter memCounter = new PerformanceCounter("Memory", "Available MBytes"))
            {
                return (long)memCounter.NextValue();
            }
        }

        // Get Total RAM (MB)
        public static long GetTotalMemory()
        {
            return new Microsoft.VisualBasic.Devices.ComputerInfo().TotalPhysicalMemory / (1024 * 1024);
        }

        // Get System Uptime (Seconds)
        public static long GetSystemUptime()
        {
            return Environment.TickCount64 / 1000;
        }

        // Get Total Disk Space (GB)
        public static long GetTotalDiskSpace(string drive = "C")
        {
            DriveInfo driveInfo = new DriveInfo(drive);
            return driveInfo.TotalSize / (1024 * 1024 * 1024);
        }

        // Get Free Disk Space (GB)
        public static long GetFreeDiskSpace(string drive = "C")
        {
            DriveInfo driveInfo = new DriveInfo(drive);
            return driveInfo.AvailableFreeSpace / (1024 * 1024 * 1024);
        }

        // Get System IP Address
        public static string GetIPAddress()
        {
            string ip = "";
            foreach (IPAddress addr in Dns.GetHostAddresses(Dns.GetHostName()))
            {
                if (addr.AddressFamily == System.Net.Sockets.AddressFamily.InterNetwork)
                {
                    ip = addr.ToString();
                    break;
                }
            }
            return ip;
        }

        // Get MAC Address
        public static string GetMACAddress()
        {
            foreach (NetworkInterface nic in NetworkInterface.GetAllNetworkInterfaces())
            {
                if (nic.OperationalStatus == OperationalStatus.Up)
                {
                    return BitConverter.ToString(nic.GetPhysicalAddress().GetAddressBytes());
                }
            }
            return "N/A";
        }

        // List Running Processes
        public static string ListRunningProcesses()
        {
            StringBuilder sb = new StringBuilder();
            foreach (Process process in Process.GetProcesses())
            {
                sb.AppendLine($"{process.ProcessName} (PID: {process.Id})");
            }
            return sb.ToString();
        }

        // Kill Process by Name
        public static string KillProcess(string processName)
        {
            try
            {
                foreach (Process proc in Process.GetProcessesByName(processName))
                {
                    proc.Kill();
                    return $"Successfully killed {processName} (PID: {proc.Id})";
                }
                return $"Process {processName} not found.";
            }
            catch (Exception ex)
            {
                return $"Error: {ex.Message}";
            }
        }

        // Get Environment Variables
        public static string GetEnvironmentVariable(string variable)
        {
            return Environment.GetEnvironmentVariable(variable) ?? "Not Found";
        }
    }

    public static class NativeExports
    {
        [DllExport("GetOSVersion", CallingConvention = CallingConvention.StdCall)]
        public static IntPtr GetOSVersionExport() => Marshal.StringToHGlobalAnsi(SystemInfo.GetOSVersion());

        [DllExport("GetSystemArchitecture", CallingConvention = CallingConvention.StdCall)]
        public static IntPtr GetSystemArchitectureExport() => Marshal.StringToHGlobalAnsi(SystemInfo.GetSystemArchitecture());

        [DllExport("GetCPUUsage", CallingConvention = CallingConvention.StdCall)]
        public static float GetCPUUsageExport() => SystemInfo.GetCPUUsage();

        [DllExport("GetAvailableMemory", CallingConvention = CallingConvention.StdCall)]
        public static long GetAvailableMemoryExport() => SystemInfo.GetAvailableMemory();

        [DllExport("GetTotalMemory", CallingConvention = CallingConvention.StdCall)]
        public static long GetTotalMemoryExport() => SystemInfo.GetTotalMemory();

        [DllExport("GetSystemUptime", CallingConvention = CallingConvention.StdCall)]
        public static long GetSystemUptimeExport() => SystemInfo.GetSystemUptime();

        [DllExport("GetIPAddress", CallingConvention = CallingConvention.StdCall)]
        public static IntPtr GetIPAddressExport() => Marshal.StringToHGlobalAnsi(SystemInfo.GetIPAddress());

        [DllExport("GetMACAddress", CallingConvention = CallingConvention.StdCall)]
        public static IntPtr GetMACAddressExport() => Marshal.StringToHGlobalAnsi(SystemInfo.GetMACAddress());

        [DllExport("ListRunningProcesses", CallingConvention = CallingConvention.StdCall)]
        public static IntPtr ListRunningProcessesExport() => Marshal.StringToHGlobalAnsi(SystemInfo.ListRunningProcesses());

        [DllExport("KillProcess", CallingConvention = CallingConvention.StdCall)]
        public static IntPtr KillProcessExport([MarshalAs(UnmanagedType.LPStr)] string processName) => 
            Marshal.StringToHGlobalAnsi(SystemInfo.KillProcess(processName));

        [DllExport("GetEnvironmentVariable", CallingConvention = CallingConvention.StdCall)]
        public static IntPtr GetEnvironmentVariableExport([MarshalAs(UnmanagedType.LPStr)] string variable) =>
            Marshal.StringToHGlobalAnsi(SystemInfo.GetEnvironmentVariable(variable));
    }
}
