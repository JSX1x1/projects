using System;
using System.Runtime.InteropServices;

namespace VariableManagerDLL
{
    public static class VariableManager
    {
        // Internal static variable
        private static int storedValue = 0;

        /// <summary>
        /// Set a new value to the stored variable.
        /// </summary>
        /// <param name="newValue">The new integer value</param>
        [DllExport("SetValue", CallingConvention = CallingConvention.StdCall)]
        public static void SetValue(int newValue)
        {
            storedValue = newValue;
        }

        /// <summary>
        /// Get the current value of the stored variable.
        /// </summary>
        /// <returns>The stored integer value</returns>
        [DllExport("GetValue", CallingConvention = CallingConvention.StdCall)]
        public static int GetValue()
        {
            return storedValue;
        }

        /// <summary>
        /// Reset the stored variable to zero.
        /// </summary>
        [DllExport("ResetValue", CallingConvention = CallingConvention.StdCall)]
        public static void ResetValue()
        {
            storedValue = 0;
        }
    }
}
