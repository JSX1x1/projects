#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cstdlib>
#include <thread>
#include <chrono>

#ifdef _WIN32
    #include <windows.h>
    #include <psapi.h>
    #include <iphlpapi.h>
    #pragma comment(lib, "iphlpapi.lib")
#elif __linux__
    #include <sys/sysinfo.h>
    #include <sys/utsname.h>
    #include <unistd.h>
#endif

using namespace std;


/// IF USED ON linux: sudo apt install sysstat lshw hwinfos
/// Windows usage runs through windows.h library

/// DO NOT USE INCASE TO GATHER INFORMATION IN ATTEMPT TO MANIPULATE SOMEONE ELSES SYSTEM OR MAKING UNAUTHORIZED ACTIONS
/// THE CREATOR WILL NOT HOLD LIABLE FOR ANY CONSEQUENCES

// Get CPU Information
void getCPUInfo() {
    cout << "🔍 Fetching CPU Information...\n";
    
    #ifdef _WIN32
    SYSTEM_INFO sysInfo;
    GetSystemInfo(&sysInfo);
    
    cout << "🔹 Number of Cores: " << sysInfo.dwNumberOfProcessors << "\n";
    
    char cpuBrand[256];
    DWORD size = sizeof(cpuBrand);
    if (RegGetValueA(HKEY_LOCAL_MACHINE, "HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0",
                     "ProcessorNameString", RRF_RT_REG_SZ, nullptr, &cpuBrand, &size) == ERROR_SUCCESS) {
        cout << "🔹 Processor: " << cpuBrand << "\n";
    }
    
    #elif __linux__
    ifstream cpuinfo("/proc/cpuinfo");
    string line;
    while (getline(cpuinfo, line)) {
        if (line.find("model name") != string::npos) {
            cout << "🔹 " << line << "\n";
        }
    }
    #endif
}

// Get RAM Information
void getMemoryInfo() {
    cout << "\n🖥️ Fetching Memory Information...\n";
    
    #ifdef _WIN32
    MEMORYSTATUSEX memInfo;
    memInfo.dwLength = sizeof(MEMORYSTATUSEX);
    GlobalMemoryStatusEx(&memInfo);
    
    cout << "🔹 Total RAM: " << memInfo.ullTotalPhys / (1024 * 1024) << " MB\n";
    cout << "🔹 Available RAM: " << memInfo.ullAvailPhys / (1024 * 1024) << " MB\n";
    
    #elif __linux__
    struct sysinfo memInfo;
    sysinfo(&memInfo);
    
    cout << "🔹 Total RAM: " << memInfo.totalram / (1024 * 1024) << " MB\n";
    cout << "🔹 Free RAM: " << memInfo.freeram / (1024 * 1024) << " MB\n";
    #endif
}

// Get Disk Information
void getDiskInfo() {
    cout << "\n💾 Fetching Disk Information...\n";
    
    #ifdef _WIN32
    ULARGE_INTEGER freeBytesAvailable, totalBytes, freeBytes;
    GetDiskFreeSpaceEx("C:\\", &freeBytesAvailable, &totalBytes, &freeBytes);
    
    cout << "🔹 Total Disk Space: " << totalBytes.QuadPart / (1024 * 1024 * 1024) << " GB\n";
    cout << "🔹 Free Space: " << freeBytes.QuadPart / (1024 * 1024 * 1024) << " GB\n";
    
    #elif __linux__
    system("df -h | grep '^/'");
    #endif
}

// Get Network Information
void getNetworkInfo() {
    cout << "\n🌐 Fetching Network Information...\n";
    
    #ifdef _WIN32
    ULONG bufferSize = 15000;
    PIP_ADAPTER_INFO adapterInfo = (PIP_ADAPTER_INFO)malloc(bufferSize);
    if (GetAdaptersInfo(adapterInfo, &bufferSize) == ERROR_SUCCESS) {
        while (adapterInfo) {
            cout << "🔹 Adapter: " << adapterInfo->Description << "\n";
            cout << "🔹 IP Address: " << adapterInfo->IpAddressList.IpAddress.String << "\n";
            cout << "🔹 MAC Address: ";
            for (UINT i = 0; i < adapterInfo->AddressLength; i++) {
                printf("%02X ", adapterInfo->Address[i]);
            }
            cout << "\n";
            adapterInfo = adapterInfo->Next;
        }
    }
    free(adapterInfo);
    
    #elif __linux__
    system("ip a | grep 'inet '");
    #endif
}

// Get Running Processes
void getProcessList() {
    cout << "\n🔄 Fetching Running Processes...\n";
    
    #ifdef _WIN32
    DWORD processes[1024], processCount;
    if (EnumProcesses(processes, sizeof(processes), &processCount)) {
        processCount /= sizeof(DWORD);
        for (unsigned int i = 0; i < processCount; i++) {
            if (processes[i] != 0) {
                HANDLE hProcess = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, FALSE, processes[i]);
                if (hProcess) {
                    char processName[MAX_PATH];
                    if (GetModuleBaseName(hProcess, nullptr, processName, sizeof(processName))) {
                        cout << "🔹 PID: " << processes[i] << " | Process: " << processName << "\n";
                    }
                    CloseHandle(hProcess);
                }
            }
        }
    }
    
    #elif __linux__
    system("ps aux --sort=-%mem | head -10");
    #endif
}

// Get System Uptime
void getSystemUptime() {
    cout << "\n⏳ Fetching System Uptime...\n";
    
    #ifdef _WIN32
    ULONGLONG uptime = GetTickCount64() / 1000;
    cout << "🔹 Uptime: " << uptime / 3600 << " hours " << (uptime % 3600) / 60 << " minutes\n";
    
    #elif __linux__
    struct sysinfo info;
    sysinfo(&info);
    cout << "🔹 Uptime: " << info.uptime / 3600 << " hours " << (info.uptime % 3600) / 60 << " minutes\n";
    #endif
}

int main() {
    cout << "🛠️ Advanced System Analysis Tool 🛠️\n";
    cout << "----------------------------------\n";

    getCPUInfo();
    getMemoryInfo();
    getDiskInfo();
    getNetworkInfo();
    getProcessList();
    getSystemUptime();

    cout << "\n✅ System Analysis Complete!\n";
    return 0;
}
