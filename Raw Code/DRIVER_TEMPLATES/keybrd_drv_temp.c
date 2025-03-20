#include <ntddk.h>
#include <ntddkbd.h>

#define DEVICE_NAME L"\\Device\\SecureKeyboardDriver"
#define SYMBOLIC_LINK_NAME L"\\DosDevices\\SecureKeyboardDriver"

// Allowed keys (e.g., function keys F1-F12)
BOOLEAN IsAllowedKey(USHORT key) {
    return (key >= 0x70 && key <= 0x7B);  // F1 - F12
}

// Hooked keyboard read routine
NTSTATUS HookedKeyboardRead(PDEVICE_OBJECT DeviceObject, PIRP Irp) {
    PIO_STACK_LOCATION stack = IoGetCurrentIrpStackLocation(Irp);
    
    if (stack->MajorFunction == IRP_MJ_READ) {
        PKEYBOARD_INPUT_DATA inputData = (PKEYBOARD_INPUT_DATA)Irp->AssociatedIrp.SystemBuffer;

        for (ULONG i = 0; i < stack->Parameters.Read.Length / sizeof(KEYBOARD_INPUT_DATA); i++) {
            if (IsAllowedKey(inputData[i].MakeCode)) {
                DbgPrint("Secure Keyboard Driver: Key Pressed - 0x%X\n", inputData[i].MakeCode);
            }
        }
    }

    return IoCallDriver(DeviceObject, Irp);  // Pass the request to the original driver
}

// Driver unload routine
VOID DriverUnload(PDRIVER_OBJECT DriverObject) {
    UNICODE_STRING symLink;
    RtlInitUnicodeString(&symLink, SYMBOLIC_LINK_NAME);
    IoDeleteSymbolicLink(&symLink);
    IoDeleteDevice(DriverObject->DeviceObject);
    DbgPrint("Secure Keyboard Driver Unloaded\n");
}

// Driver entry point
NTSTATUS DriverEntry(PDRIVER_OBJECT DriverObject, PUNICODE_STRING RegistryPath) {
    UNREFERENCED_PARAMETER(RegistryPath);
    
    PDEVICE_OBJECT DeviceObject = NULL;
    UNICODE_STRING deviceName, symLink;
    
    RtlInitUnicodeString(&deviceName, DEVICE_NAME);
    RtlInitUnicodeString(&symLink, SYMBOLIC_LINK_NAME);

    NTSTATUS status = IoCreateDevice(DriverObject, 0, &deviceName, FILE_DEVICE_KEYBOARD, 0, FALSE, &DeviceObject);
    if (!NT_SUCCESS(status)) return status;

    status = IoCreateSymbolicLink(&symLink, &deviceName);
    if (!NT_SUCCESS(status)) {
        IoDeleteDevice(DeviceObject);
        return status;
    }

    DriverObject->DriverUnload = DriverUnload;
    DriverObject->MajorFunction[IRP_MJ_READ] = HookedKeyboardRead;

    DbgPrint("Secure Keyboard Driver Loaded\n");
    return STATUS_SUCCESS;
}
