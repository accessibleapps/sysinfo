import gc
import getpass
import os
import platform
import socket
import sys
import threading

import psutil

def system_info():
    return {
        'memory': memory(),
        'network': network(),
        'operating_system': operating_system(),
        'interpreter': interpreter(),
        'current_user': current_user(),
        'storage': storage(),
        'processor': processor(),
    }

def interpreter():
    return {
        'bit_width': interpreter_bit_width(),
        'recursion_limit': sys.getrecursionlimit(),
        'used_memory': interpreter_memory_used(),
        'total_objects': interpreter_total_objects(),
        'python_threads': interpreter_python_threads(),
        'operating_system_threads': interpreter_os_threads(),
        'version': interpreter_version(),
        'byte_order': interpreter_byte_order(),
        'api_version': interpreter_api_version(),
    }

def current_user():
    return {
        'username': getpass.getuser(),
    }

def memory():
    return {
        'total': memory_total(),
        'free': memory_free(),
        'used': memory_used(),
    }

def network():
    return {
        'hostname': network_hostname(),
    }

def operating_system():
    return {
        'name': platform.system(),
        'bit_width': operating_system_bit_width(),
        'kernel_version': platform.release(),
        'kernel_release': platform.version(),
    }

def storage():
    storage = {}
    partitions = []
    for partition in list_storage_partitions():
        partition['size'] = get_partition_size(partition['mountpoint'])
        partitions.append(partition)
    storage['partitions'] = partitions
    storage['total'] = sum([i['size']['total'] for i in partitions])
    return storage

def processor():
    return {
        'name': platform.processor(),
        'times': processor_times(),
    }

def processor_times():
    times = psutil.cpu_times()
    return {
        'user': times.user,
        'system': times.system,
        'idle': times.idle,
    }

def operating_system_bit_width():
    machine = platform.machine()
    if machine == 'x86':
        return 32
    elif machine == 'AMD64':
        return 64

def network_hostname():
    return socket.getfqdn()

def interpreter_bit_width():
    return int(platform.architecture()[0][:2])

def interpreter_memory_used():
    process = get_process(os.getpid())
    memory_info = process.get_memory_info()
    return memory_info[0]

def interpreter_os_threads():
    process = get_process(os.getpid())
    return len(process.get_threads())

def interpreter_python_threads():
    return len(threading.enumerate())

def interpreter_total_objects():
    return len(gc.get_objects())

def interpreter_version():
    return float('%d.%d' % sys.version_info[:2])

def interpreter_byte_order():
    return sys.byteorder

def interpreter_api_version():
    return sys.api_version

def list_storage_partitions():
    partitions = []
    for partition in psutil.disk_partitions():
        if 'fixed' not in partition.opts:
            continue
        partitions.append({
            'device': partition.device,
            'mountpoint': partition.mountpoint,
            'filesystem': partition.fstype,
        })
    return partitions

def get_partition_size(mountpoint):
    usage = psutil.disk_usage(mountpoint)
    return {
        'total': usage.total,
        'used': usage.used,
        'free': usage.free,
        'percent': usage.percent
    }

def get_process(pid):
    processes = [i for i in psutil.get_process_list() if i.pid == pid]
    if not processes:
        raise RuntimeError("No such pid: %r" % pid)
    return processes[0]

def memory_total():
    return psutil.phymem_usage()[0]

def memory_used():
    return psutil.used_phymem()

def memory_free():
    return psutil.avail_phymem()

