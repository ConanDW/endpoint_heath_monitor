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
    min_percent = 10
    min_gb = 10
    du = shutil.disk_usage(disk)
    percent_free = 100 * du.free / du.total
    gigabytes_free = du.free / 2**30
    if percent_free < min_percent or gigabytes_free < min_gb:
        return True, percent_free
    else:
        return False

def check_free_ram():
    free_ram = psutil.virtual_memory
    return free_ram

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
        (check_disk_usage("/"), "Disk is getting full."),
        (check_no_network, "No working network."),
        (check_cpu_constrained, "CPU load too high.")
    ]
    percent_free = check_disk_usage("/")
    free_ram = check_free_ram()
    everything_ok=True
    for check, msg in checks:
        if check():
          print(msg)
          everything_ok = False
    
    if not everything_ok:
        sys.exit(1)
    
    print("Everything ok.")
    print("Free Ram: {}, Free Disk Space (%): {}".format(free_ram, percent_free))
    sys.exit(0)
    

main()
