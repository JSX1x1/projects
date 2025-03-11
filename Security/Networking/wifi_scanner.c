// ONLY WORKS ON LINUX
// MISUSE FOR UNAUTHORIZED DATA THEFT OR ACCESS IS ILLEGAL THEREFORE DO NOT USE THIS FOR UNALLOWED INTENTS!

// Dependencies: sudo apt update && sudo apt install wireless-tools net-tools
// Compile: gcc wifi_scanner.c -o wifi_scanner
// sudo ./wifi_scanner

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <math.h>

#define MAX_SSID_LEN 256
#define MAX_CMD_LEN 1024

// Function to get Wi-Fi scan results using iwlist
void scan_wifi() {
    char command[MAX_CMD_LEN];
    FILE *fp;
    char buffer[MAX_CMD_LEN];
    
    // Run iwlist command (requires sudo)
    snprintf(command, sizeof(command), "sudo iwlist wlan0 scanning");

    fp = popen(command, "r");
    if (fp == NULL) {
        perror("Error executing iwlist");
        return;
    }

    printf("\n📡 Scanning for Wi-Fi Networks...\n\n");

    char ssid[MAX_SSID_LEN] = "";
    char security[MAX_SSID_LEN] = "Open";
    double frequency = 0.0;
    int signal_level = 0;
    int channel = 0;

    while (fgets(buffer, sizeof(buffer), fp) != NULL) {
        // Extract SSID
        if (strstr(buffer, "ESSID:") != NULL) {
            sscanf(buffer, " ESSID:\"%[^\"]\"", ssid);
        }

        // Extract Signal Strength
        if (strstr(buffer, "Signal level") != NULL) {
            sscanf(buffer, " Signal level=%d dBm", &signal_level);
        }

        // Extract Frequency
        if (strstr(buffer, "Frequency:") != NULL) {
            sscanf(buffer, " Frequency:%lf GHz", &frequency);
        }

        // Extract Channel
        if (strstr(buffer, "Channel") != NULL) {
            sscanf(buffer, " Channel %d", &channel);
        }

        // Extract Security Type
        if (strstr(buffer, "IE: WPA") != NULL) {
            strcpy(security, "WPA/WPA2");
        } else if (strstr(buffer, "IE: WEP") != NULL) {
            strcpy(security, "WEP");
        }

        // Print Wi-Fi details when a complete record is found
        if (strlen(ssid) > 0 && frequency > 0.0) {
            double range = calculate_range(signal_level, frequency);
            printf("📶 **SSID:** %s\n", ssid);
            printf("   🔒 Security: %s\n", security);
            printf("   📡 Signal Strength: %d dBm\n", signal_level);
            printf("   🌍 Frequency: %.2f GHz\n", frequency);
            printf("   🔄 Channel: %d\n", channel);
            printf("   📏 Estimated Range: ~%.2f meters\n", range);
            printf("--------------------------------------------------\n");

            // Reset for next entry
            memset(ssid, 0, sizeof(ssid));
            strcpy(security, "Open");
            frequency = 0.0;
            signal_level = 0;
            channel = 0;
        }
    }
    pclose(fp);
}

// Function to estimate Wi-Fi range based on signal strength
double calculate_range(int signal_level, double frequency) {
    double exponent = (27.55 - (20 * log10(frequency * 1000)) + abs(signal_level)) / 20.0;
    return pow(10.0, exponent);  // Distance in meters
}

// Function to measure network latency using ping
void check_latency() {
    char command[MAX_CMD_LEN];
    FILE *fp;
    char buffer[MAX_CMD_LEN];
    double latency = -1.0;

    // Get default gateway IP
    snprintf(command, sizeof(command), "ip route | grep default | awk '{print $3}'");
    fp = popen(command, "r");
    if (fp == NULL) {
        perror("Error retrieving gateway IP");
        return;
    }

    char gateway_ip[64];
    if (fgets(gateway_ip, sizeof(gateway_ip), fp) == NULL) {
        printf("⚠ No network detected.\n");
        pclose(fp);
        return;
    }
    gateway_ip[strcspn(gateway_ip, "\n")] = '\0'; // Remove newline
    pclose(fp);

    printf("\n🌐 **Checking network latency to gateway: %s**\n", gateway_ip);

    // Ping the gateway
    snprintf(command, sizeof(command), "ping -c 1 %s | grep time=", gateway_ip);
    fp = popen(command, "r");
    if (fp == NULL) {
        perror("Error executing ping");
        return;
    }

    while (fgets(buffer, sizeof(buffer), fp) != NULL) {
        sscanf(buffer, "64 bytes from %*s: icmp_seq=1 ttl=%*d time=%lf ms", &latency);
    }
    pclose(fp);

    if (latency > 0.0) {
        printf("⚡ **Latency:** %.2f ms\n", latency);
    } else {
        printf("⚠ Could not measure latency. Network might be unstable.\n");
    }
}

// Function to detect Wi-Fi interface name dynamically
void detect_wifi_interface() {
    char command[MAX_CMD_LEN] = "iw dev | grep Interface | awk '{print $2}'";
    FILE *fp = popen(command, "r");
    char interface[32];

    if (fp == NULL || fgets(interface, sizeof(interface), fp) == NULL) {
        printf("⚠ No Wi-Fi interface detected.\n");
        return;
    }

    interface[strcspn(interface, "\n")] = '\0'; // Remove newline
    printf("\n🖧 **Detected Wi-Fi Interface:** %s\n", interface);
    pclose(fp);
}

int main() {
    printf("=========================================\n");
    printf("  📡 Advanced Wi-Fi Scanner & Analyzer  \n");
    printf("=========================================\n");

    detect_wifi_interface();
    scan_wifi();
    check_latency();

    printf("\n✅ **Scan Completed.**\n");
    return 0;
}
