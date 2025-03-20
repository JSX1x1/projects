#include <ntddk.h>

#define DEVICE_NAME L"\\Device\\MemoryManagerDriver"
#define SYMBOLIC_LINK_NAME L"\\DosDevices\\MemoryManager"

#define IOCTL_ALLOCATE_MEMORY CTL_CODE(FILE_DEVICE_UNKNOWN, 0x800, METHOD_BUFFERED, FILE_ANY_ACCESS)
#define IOCTL_FREE_MEMORY CTL_CODE(FILE_DEVICE_UNKNOWN, 0x801, METHOD_BUFFERED, FILE_ANY_ACCESS)
#define IOCTL_READ_PROCESS_MEMORY CTL_CODE(FILE_DEVICE_UNKNOWN, 0x802, METHOD_BUFFERED, FILE_ANY_ACCESS)
#define IOCTL_WRITE_PROCESS_MEMORY CTL_CODE(FILE_DEVICE_UNKNOWN, 0x803, METHOD_BUFFERED, FILE_ANY_ACCESS)

typedef struct _MEMORY_REQUEST {
    ULONG_PTR Address;
    SIZE_T Size;
} MEMORY_REQUEST, *PMEMORY_REQUEST;

PVOID g_AllocatedMemory = NULL;  // Global allocated memory pointer

NTSTATUS AllocateKernelMemory(PIRP Irp, PIO_STACK_LOCATION Stack) {
    SIZE_T size = *(SIZE_T*)Irp->AssociatedIrp.SystemBuffer;

    if (size > 0 && size <= PAGE_SIZE) {  // Restrict large allocations
        g_AllocatedMemory = ExAllocatePool2(POOL_FLAG_NON_PAGED, size, 'MemD');
        if (g_AllocatedMemory) {
            RtlZeroMemory(g_AllocatedMemory, size);
            KdPrint(("Allocated %llu bytes at %p\n", size, g_AllocatedMemory));
            return STATUS_SUCCESS;
        }
    }
    return STATUS_INSUFFICIENT_RESOURCES;
}

NTSTATUS FreeKernelMemory() {
    if (g_AllocatedMemory) {
        ExFreePoolWithTag(g_AllocatedMemory, 'MemD');
        g_AllocatedMemory = NULL;
        KdPrint(("Kernel memory freed.\n"));
        return STATUS_SUCCESS;
    }
    return STATUS_UNSUCCESSFUL;
}

NTSTATUS ReadProcessMemory(PIRP Irp, PIO_STACK_LOCATION Stack) {
    PMEMORY_REQUEST request = (PMEMORY_REQUEST)Irp->AssociatedIrp.SystemBuffer;
    PEPROCESS targetProcess;
    SIZE_T bytesRead = 0;
    NTSTATUS status = PsLookupProcessByProcessId((HANDLE)request->Address, &targetProcess);

    if (NT_SUCCESS(status)) {
        status = MmCopyVirtualMemory(targetProcess, (PVOID)request->Address,
                                     PsGetCurrentProcess(), (PVOID)request->Size,
                                     request->Size, KernelMode, &bytesRead);
        ObDereferenceObject(targetProcess);
    }
    return status;
}

NTSTATUS WriteProcessMemory(PIRP Irp, PIO_STACK_LOCATION Stack) {
    PMEMORY_REQUEST request = (PMEMORY_REQUEST)Irp->AssociatedIrp.SystemBuffer;
    PEPROCESS targetProcess;
    SIZE_T bytesWritten = 0;
    NTSTATUS status = PsLookupProcessByProcessId((HANDLE)request->Address, &targetProcess);

    if (NT_SUCCESS(status)) {
        status = MmCopyVirtualMemory(PsGetCurrentProcess(), (PVOID)request->Size,
                                     targetProcess, (PVOID)request->Address,
                                     request->Size, KernelMode, &bytesWritten);
        ObDereferenceObject(targetProcess);
    }
    return status;
}

NTSTATUS IoctlHandler(PDEVICE_OBJECT DeviceObject, PIRP Irp) {
    PIO_STACK_LOCATION stack = IoGetCurrentIrpStackLocation(Irp);
    NTSTATUS status = STATUS_INVALID_PARAMETER;

    switch (stack->Parameters.DeviceIoControl.IoControlCode) {
        case IOCTL_ALLOCATE_MEMORY:
            status = AllocateKernelMemory(Irp, stack);
            break;
        case IOCTL_FREE_MEMORY:
            status = FreeKernelMemory();
            break;
        case IOCTL_READ_PROCESS_MEMORY:
            status = ReadProcessMemory(Irp, stack);
            break;
        case IOCTL_WRITE_PROCESS_MEMORY:
            status = WriteProcessMemory(Irp, stack);
            break;
    }
    
    Irp->IoStatus.Status = status;
    Irp->IoStatus.Information = 0;
    IoCompleteRequest(Irp, IO_NO_INCREMENT);
    return status;
}

NTSTATUS DriverEntry(PDRIVER_OBJECT DriverObject, PUNICODE_STRING RegistryPath) {
    UNICODE_STRING devName = RTL_CONSTANT_STRING(DEVICE_NAME);
    UNICODE_STRING symLink = RTL_CONSTANT_STRING(SYMBOLIC_LINK_NAME);
    PDEVICE_OBJECT DeviceObject = NULL;
    NTSTATUS status = IoCreateDevice(DriverObject, 0, &devName, FILE_DEVICE_UNKNOWN, 0, FALSE, &DeviceObject);

    if (!NT_SUCCESS(status)) return status;
    status = IoCreateSymbolicLink(&symLink, &devName);
    if (!NT_SUCCESS(status)) {
        IoDeleteDevice(DeviceObject);
        return status;
    }

    DriverObject->MajorFunction[IRP_MJ_DEVICE_CONTROL] = IoctlHandler;
    DriverObject->DriverUnload = [](PDRIVER_OBJECT obj) {
        IoDeleteSymbolicLink(&symLink);
        IoDeleteDevice(obj->DeviceObject);
    };

    return STATUS_SUCCESS;
}
