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
        return False, percent_free()

def check_free_ram():
    """Returns free ram."""
    free_ram = psutil.virtual_memory()
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
    cpu_usage = psutil.cpu_percent()
    if psutil.cpu_percent(1) > 75:
        return True, cpu_usage
    else:
        return False, cpu_usage

def main():
    checks = [
        (check_reboot(), "Pending Reboot."),
        (check_disk_usage("/"), "Disk is getting full."),
        (check_no_network(), "No working network."),
        (check_cpu_constrained(), "CPU load too high.")
    ]
    percent_free = check_disk_usage("/")[1]
    free_ram = check_free_ram()[2]
    free_cpu = check_cpu_constrained()[1]
    free_cpu = 100.0 - free_cpu
    everything_ok=True
    for check, msg in checks:
        if check:
          print(msg)
          everything_ok = False
    
    if not everything_ok:
        print("Free Ram (%): {}, Free Disk Space (%): {}, CPU Free (%): {}".format(str(free_ram), percent_free, free_cpu))
        sys.exit(1)
    
    print("Everything ok.")
    print("Free Ram (%): {}, Free Disk Space (%): {}, CPU Free (%): {}".format(str(free_ram), percent_free, free_cpu))
    sys.exit(0)
    

main()
