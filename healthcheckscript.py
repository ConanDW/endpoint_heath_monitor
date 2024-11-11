#!/usr/bin/env python3
import shutil
import psutil
import socket
import os
import sys
    
def check_reboot():
    """Returns true if the computer has a pending reboot."""
    return os.path.exists("/run/reboot-required")
    
def check_disk_usage(disk):
    """Returns true if there isn't enough disk space, False otherwise."""
    du = shutil.disk_usage(disk)
    percent_free = 100 * du.free / du.total
    gigabytes_free = du.free / 2**30
    if percent_free < min_percent or gigabytes_free < min_gb:
        return True
    else:
        return False
    
def check_no_network():
    """Returns True if it fails to resolve Google's URL, False otherwise."""
    try:
        socket.gethostbyname("www.google.com")
        return False
    except:
        return True
    
def check_cpu_constrained():
    """Returns True if the cpu is having too much usage, False otherwise."""
    return psutil.cpu_percent(1) > 75
    
def main():
    checks = [
        (check_reboot, "Pending Reboot."),
        (check_root_full, "Root partition full."),
        (check_no_network, "No working network."),
        (check_cpu_constrained, "CPU load too high.")
    ]
    everything_ok=True
    for check, msg in checks():
        if check():
          print(msg)
          everything_ok = False
    
    if not everything_ok:
        sys.exit(1)
    
    print("Everything ok.")
    sys.exit(0)
    
    
main()
