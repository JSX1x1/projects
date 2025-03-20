#include <ntddk.h>

#define DEVICE_NAME L"\\Device\\MyIoctlDriver"
#define SYMBOLIC_NAME L"\\DosDevices\\MyIoctlDriver"

// Define custom IOCTL codes
#define IOCTL_SEND_DATA CTL_CODE(FILE_DEVICE_UNKNOWN, 0x800, METHOD_BUFFERED, FILE_ANY_ACCESS)
#define IOCTL_GET_DATA  CTL_CODE(FILE_DEVICE_UNKNOWN, 0x801, METHOD_BUFFERED, FILE_ANY_ACCESS)

// Buffer to store received data
CHAR GlobalBuffer[256] = "Default Kernel Message";

// Function prototypes
NTSTATUS DriverEntry(PDRIVER_OBJECT DriverObject, PUNICODE_STRING RegistryPath);
VOID DriverUnload(PDRIVER_OBJECT DriverObject);
NTSTATUS IoctlDispatch(PDEVICE_OBJECT DeviceObject, PIRP Irp);
NTSTATUS CreateCloseHandler(PDEVICE_OBJECT DeviceObject, PIRP Irp);

// Driver Entry Point
NTSTATUS DriverEntry(PDRIVER_OBJECT DriverObject, PUNICODE_STRING RegistryPath) {
    UNREFERENCED_PARAMETER(RegistryPath);
    
    NTSTATUS status;
    PDEVICE_OBJECT DeviceObject = NULL;

    // Create device
    status = IoCreateDevice(
        DriverObject,
        0,
        (PUNICODE_STRING)&DEVICE_NAME,
        FILE_DEVICE_UNKNOWN,
        0,
        FALSE,
        &DeviceObject
    );

    if (!NT_SUCCESS(status)) {
        DbgPrint("[Driver] Failed to create device\n");
        return status;
    }

    // Create symbolic link
    status = IoCreateSymbolicLink((PUNICODE_STRING)&SYMBOLIC_NAME, (PUNICODE_STRING)&DEVICE_NAME);
    if (!NT_SUCCESS(status)) {
        DbgPrint("[Driver] Failed to create symbolic link\n");
        IoDeleteDevice(DeviceObject);
        return status;
    }

    // Set up dispatch functions
    DriverObject->MajorFunction[IRP_MJ_CREATE] = CreateCloseHandler;
    DriverObject->MajorFunction[IRP_MJ_CLOSE] = CreateCloseHandler;
    DriverObject->MajorFunction[IRP_MJ_DEVICE_CONTROL] = IoctlDispatch;
    DriverObject->DriverUnload = DriverUnload;

    DbgPrint("[Driver] Loaded successfully\n");
    return STATUS_SUCCESS;
}

// Handle Create and Close
NTSTATUS CreateCloseHandler(PDEVICE_OBJECT DeviceObject, PIRP Irp) {
    UNREFERENCED_PARAMETER(DeviceObject);

    Irp->IoStatus.Status = STATUS_SUCCESS;
    Irp->IoStatus.Information = 0;
    IoCompleteRequest(Irp, IO_NO_INCREMENT);
    return STATUS_SUCCESS;
}

// Handle IOCTL requests
NTSTATUS IoctlDispatch(PDEVICE_OBJECT DeviceObject, PIRP Irp) {
    UNREFERENCED_PARAMETER(DeviceObject);

    PIO_STACK_LOCATION IoStackLocation = IoGetCurrentIrpStackLocation(Irp);
    ULONG IoControlCode = IoStackLocation->Parameters.DeviceIoControl.IoControlCode;
    NTSTATUS Status = STATUS_INVALID_DEVICE_REQUEST;

    switch (IoControlCode) {
        case IOCTL_SEND_DATA:
            if (IoStackLocation->Parameters.DeviceIoControl.InputBufferLength > 0) {
                RtlCopyMemory(GlobalBuffer, Irp->AssociatedIrp.SystemBuffer, IoStackLocation->Parameters.DeviceIoControl.InputBufferLength);
                GlobalBuffer[IoStackLocation->Parameters.DeviceIoControl.InputBufferLength] = '\0';
                DbgPrint("[Driver] Received data: %s\n", GlobalBuffer);
                Status = STATUS_SUCCESS;
            }
            break;

        case IOCTL_GET_DATA:
            if (IoStackLocation->Parameters.DeviceIoControl.OutputBufferLength >= sizeof(GlobalBuffer)) {
                RtlCopyMemory(Irp->AssociatedIrp.SystemBuffer, GlobalBuffer, sizeof(GlobalBuffer));
                Irp->IoStatus.Information = sizeof(GlobalBuffer);
                DbgPrint("[Driver] Sent data: %s\n", GlobalBuffer);
                Status = STATUS_SUCCESS;
            }
            break;

        default:
            DbgPrint("[Driver] Unknown IOCTL request\n");
            break;
    }

    Irp->IoStatus.Status = Status;
    IoCompleteRequest(Irp, IO_NO_INCREMENT);
    return Status;
}

// Driver Unload
VOID DriverUnload(PDRIVER_OBJECT DriverObject) {
    IoDeleteSymbolicLink((PUNICODE_STRING)&SYMBOLIC_NAME);
    IoDeleteDevice(DriverObject->DeviceObject);
    DbgPrint("[Driver] Unloaded successfully\n");
}
