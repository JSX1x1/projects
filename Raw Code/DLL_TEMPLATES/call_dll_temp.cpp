#include <iostream>
#include <windows.h>

// Define a function pointer for a generic DLL function (Must be adjusted per DLL)
typedef int (*GenericFunction)(); // Adjust return type and parameters as needed

int main() {
    // Specify the DLL name (Adjust this)
    const char* dllPath = "YourDLL.dll";  // Change this to your actual DLL filename

    // Load the DLL dynamically
    HMODULE hDLL = LoadLibrary(dllPath);

    // Check if the DLL was loaded successfully
    if (!hDLL) {
        std::cerr << "Failed to load DLL: " << dllPath << "\n";
        return 1; // Exit with error
    }
    std::cout << "Successfully loaded: " << dllPath << "\n";

    // Specify the function name inside the DLL (Adjust this)
    const char* functionName = "YourFunction"; // Change to the actual function name in the DLL

    // Get the function address
    GenericFunction functionPointer = (GenericFunction)GetProcAddress(hDLL, functionName);

    // Check if the function was found
    if (!functionPointer) {
        std::cerr << "Failed to find function: " << functionName << " in " << dllPath << "\n";
        FreeLibrary(hDLL); // Unload the DLL before exiting
        return 1;
    }
    std::cout << "Successfully found function: " << functionName << "\n";

    // Call the function (Adjust arguments if needed)
    int result = functionPointer(); // Adjust as per the actual function signature
    std::cout << "Function returned: " << result << "\n";

    // Unload the DLL after use
    FreeLibrary(hDLL);
    std::cout << "DLL unloaded.\n";

    return 0;
}
