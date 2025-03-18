#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cstdlib>
#include <thread>
#include <chrono>
#include <iomanip>
#include <filesystem>

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
namespace fs = std::filesystem;

// File for logging system information
ofstream logFile("system_report.txt");

void log(const string& text) {
    cout << text << endl;
    logFile << text << endl;
}

// Get CPU Information
void getCPUInfo() {
    log("\n🔍 Fetching CPU Information...");
    
    #ifdef _WIN32
    SYSTEM_INFO sysInfo;
    GetSystemInfo(&sysInfo);
    log("🔹 Number of Cores: " + to_string(sysInfo.dwNumberOfProcessors));

    char cpuBrand[256];
    DWORD size = sizeof(cpuBrand);
    if (RegGetValueA(HKEY_LOCAL_MACHINE, "HARDWARE\\DESCRIPTION\\System\\CentralProcessor\\0",
                     "ProcessorNameString", RRF_RT_REG_SZ, nullptr, &cpuBrand, &size) == ERROR_SUCCESS) {
        log("🔹 Processor: " + string(cpuBrand));
    }
    
    #elif __linux__
    ifstream cpuinfo("/proc/cpuinfo");
    string line;
    while (getline(cpuinfo, line)) {
        if (line.find("model name") != string::npos) {
            log("🔹 " + line);
            break;
        }
    }
    #endif
}

// Get RAM Information
void getMemoryInfo() {
    log("\n🖥️ Fetching Memory Information...");
    
    #ifdef _WIN32
    MEMORYSTATUSEX memInfo;
    memInfo.dwLength = sizeof(MEMORYSTATUSEX);
    GlobalMemoryStatusEx(&memInfo);
    
    log("🔹 Total RAM:      " + to_string(memInfo.ullTotalPhys / (1024 * 1024)) + " MB");
    log("🔹 Available RAM:  " + to_string(memInfo.ullAvailPhys / (1024 * 1024)) + " MB");
    
    #elif __linux__
    struct sysinfo memInfo;
    sysinfo(&memInfo);
    
    log("🔹 Total RAM:      " + to_string(memInfo.totalram / (1024 * 1024)) + " MB");
    log("🔹 Free RAM:       " + to_string(memInfo.freeram / (1024 * 1024)) + " MB");
    #endif
}

// Get Disk Information using C++17 filesystem
void getDiskInfo() {
    log("\n💾 Fetching Disk Information...");
    try {
        fs::space_info diskSpace = fs::space("/");
        log("🔹 Total Space:    " + to_string(diskSpace.capacity / (1024 * 1024 * 1024)) + " GB");
        log("🔹 Free Space:     " + to_string(diskSpace.free / (1024 * 1024 * 1024)) + " GB");
    } catch (exception& e) {
        log("❌ Error fetching disk info: " + string(e.what()));
    }
}

// Get Network Information
void getNetworkInfo() {
    log("\n🌐 Fetching Network Information...");
    
    #ifdef _WIN32
    ULONG bufferSize = 15000;
    PIP_ADAPTER_INFO adapterInfo = (PIP_ADAPTER_INFO)malloc(bufferSize);
    if (GetAdaptersInfo(adapterInfo, &bufferSize) == ERROR_SUCCESS) {
        while (adapterInfo) {
            log("🔹 Adapter:       " + string(adapterInfo->Description));
            log("🔹 IP Address:    " + string(adapterInfo->IpAddressList.IpAddress.String));
            log("🔹 MAC Address:   ");
            for (UINT i = 0; i < adapterInfo->AddressLength; i++) {
                printf("%02X ", adapterInfo->Address[i]);
            }
            log("\n");
            adapterInfo = adapterInfo->Next;
        }
    }
    free(adapterInfo);
    
    #elif __linux__
    log("🔹 Active Network Interfaces & IPs:");
    system("ip -o -4 addr show | awk '{print $2 \" -> \" $4}'");
    #endif
}

// Get Running Processes (Improved)
void getProcessList() {
    log("\n🔄 Fetching Running Processes...");
    
    #ifdef _WIN32
    DWORD processes[1024], processCount;
    if (EnumProcesses(processes, sizeof(processes), &processCount)) {
        processCount /= sizeof(DWORD);
        for (unsigned int i = 0; i < min(processCount, 10U); i++) { // Limit to top 10 processes
            if (processes[i] != 0) {
                HANDLE hProcess = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, FALSE, processes[i]);
                if (hProcess) {
                    char processName[MAX_PATH];
                    PROCESS_MEMORY_COUNTERS pmc;
                    if (GetModuleBaseName(hProcess, nullptr, processName, sizeof(processName)) &&
                        GetProcessMemoryInfo(hProcess, &pmc, sizeof(pmc))) {
                        log("🔹 PID: " + to_string(processes[i]) + " | Process: " + processName + 
                            " | Memory Usage: " + to_string(pmc.WorkingSetSize / (1024 * 1024)) + " MB");
                    }
                    CloseHandle(hProcess);
                }
            }
        }
    }
    
    #elif __linux__
    log("🔹 Top Processes (CPU & Memory Usage):");
    system("top -b -n 1 | head -15");
    #endif
}

// Get System Uptime
void getSystemUptime() {
    log("\n⏳ Fetching System Uptime...");
    
    #ifdef _WIN32
    ULONGLONG uptime = GetTickCount64() / 1000;
    log("🔹 Uptime: " + to_string(uptime / 3600) + " hours " + to_string((uptime % 3600) / 60) + " minutes");
    
    #elif __linux__
    struct sysinfo info;
    sysinfo(&info);
    log("🔹 Uptime: " + to_string(info.uptime / 3600) + " hours " + to_string((info.uptime % 3600) / 60) + " minutes");
    #endif
}

// Main Function with Multithreading
int main() {
    cout << "🛠️ Advanced System Analysis Tool 🛠️\n";
    cout << "----------------------------------\n";

    // Run all system checks in parallel
    thread t1(getCPUInfo);
    thread t2(getMemoryInfo);
    thread t3(getDiskInfo);
    thread t4(getNetworkInfo);
    thread t5(getProcessList);
    thread t6(getSystemUptime);

    // Wait for all threads to finish
    t1.join();
    t2.join();
    t3.join();
    t4.join();
    t5.join();
    t6.join();

    log("\n✅ System Analysis Complete! Report saved as 'system_report.txt'.");
    logFile.close();
    return 0;
}
