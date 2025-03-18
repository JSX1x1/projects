// This dll is used as template for value exports in different dll calls in different files and programms

using System;
using System.Runtime.InteropServices;
using System.Text;

namespace ExportedFunctionsDLL
{
    public static class ExportedFunctions
    {
        // Basic Math Functions
        [DllExport("Add", CallingConvention = CallingConvention.StdCall)]
        public static int Add(int a, int b) => a + b;

        [DllExport("Subtract", CallingConvention = CallingConvention.StdCall)]
        public static int Subtract(int a, int b) => a - b;

        [DllExport("Multiply", CallingConvention = CallingConvention.StdCall)]
        public static int Multiply(int a, int b) => a * b;

        [DllExport("Divide", CallingConvention = CallingConvention.StdCall)]
        public static double Divide(int a, int b) => (b != 0) ? (double)a / b : 0;

        // String Operations
        [DllExport("ReverseString", CallingConvention = CallingConvention.StdCall)]
        public static string ReverseString([MarshalAs(UnmanagedType.LPStr)] string input)
        {
            char[] charArray = input.ToCharArray();
            Array.Reverse(charArray);
            return new string(charArray);
        }

        [DllExport("ToUpperCase", CallingConvention = CallingConvention.StdCall)]
        public static string ToUpperCase([MarshalAs(UnmanagedType.LPStr)] string input)
        {
            return input.ToUpper();
        }

        // System Information
        [DllExport("GetSystemTime", CallingConvention = CallingConvention.StdCall)]
        public static void GetSystemTime(out SYSTEMTIME time)
        {
            GetSystemTimeNative(out time);
        }

        [DllImport("kernel32.dll")]
        private static extern void GetSystemTimeNative(out SYSTEMTIME time);

        public struct SYSTEMTIME
        {
            public ushort Year;
            public ushort Month;
            public ushort DayOfWeek;
            public ushort Day;
            public ushort Hour;
            public ushort Minute;
            public ushort Second;
            public ushort Milliseconds;
        }

        // Memory Management
        [DllExport("AllocateMemory", CallingConvention = CallingConvention.StdCall)]
        public static IntPtr AllocateMemory(int size)
        {
            return Marshal.AllocHGlobal(size);
        }

        [DllExport("FreeMemory", CallingConvention = CallingConvention.StdCall)]
        public static void FreeMemory(IntPtr ptr)
        {
            if (ptr != IntPtr.Zero)
                Marshal.FreeHGlobal(ptr);
        }

        // Random Number Generator
        private static Random random = new Random();

        [DllExport("GetRandomNumber", CallingConvention = CallingConvention.StdCall)]
        public static int GetRandomNumber(int min, int max)
        {
            return random.Next(min, max);
        }
    }
}
