#include <ntddk.h>

// Driver unload function (called when driver is unloaded)
VOID DriverUnload(PDRIVER_OBJECT DriverObject) {
    UNREFERENCED_PARAMETER(DriverObject);
    DbgPrint("[Driver] Unloaded successfully.\n");
}

// Driver entry point (called when driver loads)
NTSTATUS DriverEntry(PDRIVER_OBJECT DriverObject, PUNICODE_STRING RegistryPath) {
    UNREFERENCED_PARAMETER(RegistryPath);

    DbgPrint("[Driver] Loaded successfully.\n");

    // Set the unload function
    DriverObject->DriverUnload = DriverUnload;

    return STATUS_SUCCESS;  // Successfully loaded
}
