import socket
import psutil
import ipaddress

def get_local_ip():
    # Get the local machine's IP address
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # Change to the local network interface
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'  # fallback to localhost
    finally:
        s.close()
    return ip

def get_subnet_mask(interface_name="eth0"):
    # Get the subnet mask of the local network interface
    addrs = psutil.net_if_addrs()
    if interface_name in addrs:
        for addr in addrs[interface_name]:
            if addr.family == socket.AF_INET:
                return addr.netmask
    return None

def calculate_network_range(local_ip, subnet_mask):
    # Calculate the network range based on IP and subnet mask
    ip_obj = ipaddress.IPv4Interface(f"{local_ip}/{subnet_mask}")
    network_range = ip_obj.network
    return network_range

if __name__ == "__main__":
    local_ip = get_local_ip()
    subnet_mask = get_subnet_mask("eth0")  # Change this if using a different interface (e.g., 'wlan0' for Wi-Fi)

    if subnet_mask:
        network_range = calculate_network_range(local_ip, subnet_mask)
        # Print the local IP and the network range in CIDR notation
        print(f"Local IP Address: {local_ip}")
        print(f"Subnet Mask: {subnet_mask}")
        print(f"Network Range: {network_range}")
    else:
        print("Could not retrieve the subnet mask.")
