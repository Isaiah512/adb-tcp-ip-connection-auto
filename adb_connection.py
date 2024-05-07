import subprocess
import re
import sys
import time
import msvcrt

def get_phone_local_ip():
    try:
        result = subprocess.run(['adb', 'shell', 'ip', '-f', 'inet', 'addr', 'show'], capture_output=True, text=True)
        
        if result.returncode == 0:
            ip_address_match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)/\d+.*wlan0', result.stdout)
            if ip_address_match:
                return ip_address_match.group(1)
            else:
                return "IP address not found for wlan0 interface."
        else:
            return "Error: Unable to execute adb command."
    except FileNotFoundError:
        return "Error: ADB not found. Please make sure ADB is installed and added to your PATH."

def set_adb_tcpip(ip_address, port):
    try:
        subprocess.run(['adb', 'tcpip', str(port)], capture_output=True, text=True)
        print("ADB set up over TCP/IP on port", port)
    except Exception as e:
        print("Error setting up ADB over TCP/IP:", str(e))
        sys.exit(1)

def connect_to_phone_via_adb(ip_address, port):
    try:
        result = subprocess.run(['adb', 'connect', f"{ip_address}:{port}"], capture_output=True, text=True)
        
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print("Error: Unable to connect to phone via ADB over TCP/IP.")
            stop_adb_connection()
            sys.exit(1)
    except FileNotFoundError:
        print("Error: ADB not found. Please make sure ADB is installed and added to your PATH.")
        sys.exit(1)

def stop_adb_connection():
    try:
        subprocess.run(['adb', 'disconnect'], check=True)
        print("ADB connection stopped.")
    except subprocess.CalledProcessError:
        print("Error: Unable to stop ADB connection.")

def is_key_pressed():
    return msvcrt.kbhit()
def get_key_pressed():
    return msvcrt.getch()

local_ip = get_phone_local_ip()
if local_ip.startswith("Error"):
    print(local_ip)
    sys.exit(1)
else:
    print("Phone's Local IP Address:", local_ip)

port = 5555  # Replace with the desired port number
set_adb_tcpip(local_ip, port)
connection_result = connect_to_phone_via_adb(local_ip, port)

if connection_result.startswith("connected"):
    print("ADB connection successful:", connection_result)
else:
    print("ADB connection result:", connection_result)
    stop_adb_connection()

print("Press 'x' to stop the connection.")
while True:
    if is_key_pressed():
        key = get_key_pressed()
        if key.lower() == b'x' or key == b'\r':
            stop_adb_connection()
            break
