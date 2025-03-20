#include <windows.h>
#include <stdio.h>
#include <stdlib.h>

#define DEVICE_NAME  "\\\\.\\MyDriver"  // Modify this based on your driver
#define IOCTL_CUSTOM_OPERATION CTL_CODE(FILE_DEVICE_UNKNOWN, 0x800, METHOD_BUFFERED, FILE_ANY_ACCESS)

void communicateWithIOCTL();
void readWriteDevice();
void registryInteraction();

int main(int argc, char *argv[]) {
    int choice;

    printf("Universal User-Mode Driver Communicator\n");
    printf("[1] Communicate via IOCTL\n");
    printf("[2] Read/Write to Device\n");
    printf("[3] Registry Interaction (for filter drivers)\n");
    printf("Select an option: ");
    scanf("%d", &choice);

    switch (choice) {
        case 1:
            communicateWithIOCTL();
            break;
        case 2:
            readWriteDevice();
            break;
        case 3:
            registryInteraction();
            break;
        default:
            printf("Invalid choice.\n");
    }

    return 0;
}

// 🔹 IOCTL-based communication with a driver
void communicateWithIOCTL() {
    HANDLE hDevice;
    DWORD bytesReturned;
    char inputBuffer[128] = "Hello, Driver!";
    char outputBuffer[128] = {0};

    hDevice = CreateFile(DEVICE_NAME, GENERIC_READ | GENERIC_WRITE, 0, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hDevice == INVALID_HANDLE_VALUE) {
        printf("Failed to open device: %d\n", GetLastError());
        return;
    }

    if (DeviceIoControl(hDevice, IOCTL_CUSTOM_OPERATION, inputBuffer, sizeof(inputBuffer),
                        outputBuffer, sizeof(outputBuffer), &bytesReturned, NULL)) {
        printf("IOCTL Success! Response: %s\n", outputBuffer);
    } else {
        printf("IOCTL failed: %d\n", GetLastError());
    }

    CloseHandle(hDevice);
}

// 🔹 Direct Read/Write to a Device Driver
void readWriteDevice() {
    HANDLE hDevice;
    DWORD bytesWritten, bytesRead;
    char writeBuffer[128] = "Data to write";
    char readBuffer[128] = {0};

    hDevice = CreateFile(DEVICE_NAME, GENERIC_READ | GENERIC_WRITE, 0, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hDevice == INVALID_HANDLE_VALUE) {
        printf("Failed to open device: %d\n", GetLastError());
        return;
    }

    if (WriteFile(hDevice, writeBuffer, sizeof(writeBuffer), &bytesWritten, NULL)) {
        printf("Data written to device successfully.\n");
    } else {
        printf("Write failed: %d\n", GetLastError());
    }

    if (ReadFile(hDevice, readBuffer, sizeof(readBuffer), &bytesRead, NULL)) {
        printf("Data read from device: %s\n", readBuffer);
    } else {
        printf("Read failed: %d\n", GetLastError());
    }

    CloseHandle(hDevice);
}

// 🔹 Registry Interaction for Registry Filter Drivers
void registryInteraction() {
    HKEY hKey;
    const char *subKey = "SOFTWARE\\MyDriverTest";
    const char *valueName = "TestValue";
    DWORD data = 1234;
    DWORD dataSize = sizeof(data);

    if (RegCreateKeyEx(HKEY_LOCAL_MACHINE, subKey, 0, NULL, REG_OPTION_NON_VOLATILE, KEY_WRITE, NULL, &hKey, NULL) == ERROR_SUCCESS) {
        if (RegSetValueEx(hKey, valueName, 0, REG_DWORD, (BYTE *)&data, dataSize) == ERROR_SUCCESS) {
            printf("Registry value written successfully.\n");
        } else {
            printf("Failed to set registry value.\n");
        }
        RegCloseKey(hKey);
    } else {
        printf("Failed to create registry key.\n");
    }
}
