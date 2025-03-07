import sys
import scapy.all as scapy
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton
from PyQt6.QtCore import Qt

# Function to perform network scan and get the list of devices
def scan_network(ip_range):
    # Sending ARP requests to get information on all devices in the local network
    arp_request = scapy.ARP(pdst=ip_range)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    
    devices = []
    for element in answered_list:
        device_info = {
            "IP": element[1].psrc,
            "MAC": element[1].hwsrc,
            "Name": get_device_name(element[1].psrc)  # Get name for each device
        }
        devices.append(device_info)
    
    return devices

# Function to get the device name by sending a request and analyzing the response
def get_device_name(ip):
    try:
        # We use scapy's ICMP to query for the device name
        response = scapy.sr1(scapy.IP(dst=ip)/scapy.ICMP(), timeout=1, verbose=False)
        if response:
            return response.src  # Return the source IP as the device name
        else:
            return "Unknown"
    except:
        return "Unknown"

# PyQt6 GUI for displaying connected devices
class DeviceScannerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Network Device Scanner")
        self.setGeometry(100, 100, 600, 400)
        
        # Create a layout
        layout = QVBoxLayout()
        
        # Create a label
        self.label = QLabel("Connected Devices in Network:")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Create a button to refresh the device list
        self.refresh_button = QPushButton("Refresh Device List")
        self.refresh_button.clicked.connect(self.refresh_device_list)
        
        # Create a table to display devices
        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["IP Address", "MAC Address", "Device Name"])
        self.table.setRowCount(0)
        
        # Add components to layout
        layout.addWidget(self.label)
        layout.addWidget(self.refresh_button)
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        
        # Refresh the device list when the app starts
        self.refresh_device_list()
    
    def refresh_device_list(self):
        # Scan the local network for connected devices
        devices = scan_network("192.168.1.1/24")  # You may adjust the IP range based on your network // USE THE NETWORKRANGE RESOLVER OR TRY IT IN THE TERMINAL
        
        # Clear the current table contents
        self.table.setRowCount(0)
        
        # Populate the table with the new device list
        for device in devices:
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            self.table.setItem(row_position, 0, QTableWidgetItem(device["IP"]))
            self.table.setItem(row_position, 1, QTableWidgetItem(device["MAC"]))
            self.table.setItem(row_position, 2, QTableWidgetItem(device["Name"]))

# Main entry point to start the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Create the app window and run
    window = DeviceScannerApp()
    window.show()
    
    sys.exit(app.exec())
