#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cstdlib>
#include <thread>
#include <chrono>
#include <iomanip>

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

#if __cplusplus >= 201703L  // Check if C++17 is supported
    #include <filesystem>
    namespace fs = std::filesystem;
#else
    #error "C++17 or newer is required for std::filesystem"
#endif

using namespace std;

// Get CPU Information
void getCPUInfo() {
    cout << "\n🔍 Fetching CPU Information...\n";
    
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
            break;
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

    try {
        fs::space_info diskSpace = fs::space("."); // Use current drive
        cout << "🔹 Total Disk Space: " << diskSpace.capacity / (1024 * 1024 * 1024) << " GB\n";
        cout << "🔹 Free Space: " << diskSpace.free / (1024 * 1024 * 1024) << " GB\n";
    } catch (const exception& e) {
        cerr << "❌ Error fetching disk info: " << e.what() << "\n";
    }
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
    system("ip -4 addr show | grep 'inet '");
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
    system("ps -eo pid,comm,%mem --sort=-%mem | head -10");
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
