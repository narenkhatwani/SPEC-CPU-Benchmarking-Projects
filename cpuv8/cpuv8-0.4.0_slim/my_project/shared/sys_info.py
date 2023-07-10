#!/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
import shutil
import sys
import os

########################################################################
#                                                                      #
# Licensed per Software License Clickwrap (SPPO).PDF document          #
#                                                                      #
# PURPOSE: Provides a library of commonly used system information      #
#          routines.                                                   #
#                                                                      #
# VERSION: 1.1.5                                                       #
#                                                                      #
########################################################################

# CONSTANTS:
__version__ = "1.1.5"
ONE_GIBIBYTE = 1024 ** 3
EOL = "\n"
MILANX_MODELS = ['7773X', '7673X', '7573X', '7473X', '7373X']

LSTOPO_PATH = (
    shutil.which("lstopo-no-graphics") or shutil.which("lstopo") or ""
).strip()


def get_version():
    return __version__


def is_usr_root():
    return os.geteuid() == 0


def get_command_output_string(a_cmd):
    result = str(subprocess.check_output(a_cmd, shell=True).decode('UTF-8')).split()[0]
    return result.strip()


def get_command_output_int(a_cmd):
    return int(get_command_output_string(a_cmd))


def get_command_output_float(a_cmd):
    return float(get_command_output_string(a_cmd))


def is_32bit_support_installed(a_32bit_test_program):
    # if the grep returns something then 32-bit support is installed:
    if a_32bit_test_program == "":
        print("You must supply the fully qualified path to the 32-bit test program.")
        sys.exit(1)
    try:
        print("Attempting to launch: " + a_32bit_test_program)
        result = get_command_output_string(a_32bit_test_program)
    except (subprocess.SubprocessError, OSError):
        return False
    print(result, flush=True)
    return True


def get_cpu2017_version(a_runcpu_path):
    return get_command_output_string(a_runcpu_path + " --version | grep 'CPU2017 version:' | awk '{print $3}'")


def get_aslr():
    return get_command_output_int("sysctl kernel.randomize_va_space | awk '{ print $3 }'")


def set_aslr(a_enable):
    if a_enable:
        aslr_value = 2
    else:
        aslr_value = 0
    return get_command_output_int("sysctl -w kernel.randomize_va_space=" + str(aslr_value) + " | awk '{ print $3 }'")


def is_numactl_installed(a_print_result=True):
    try:
        numa_node_count = get_command_output_int("numactl --hardware | grep 'available:' | awk '{print $2}'")
        if a_print_result:
            print(f"numactl is installed. The number of NUMA nodes is {numa_node_count}")
        return True
    except (subprocess.SubprocessError, OSError):
        if a_print_result:
            print("numactl is NOT installed.")
        return False


def is_lstopo_installed(a_print_result=True):
    if LSTOPO_PATH:
        if a_print_result:
            print(f"lstopo is installed here: {LSTOPO_PATH}")
        return True
    else:
        if a_print_result:
            print("lstopo is NOT installed.")
        return False


def get_numa_node_count():
    if is_numactl_installed(False):
        return get_command_output_int("numactl --hardware | grep 'available:' | awk '{print $2}'")
    else:
        print("numactl must be installed for get_numa_node_count.")
        return -1


def get_os():
    return get_command_output_string("cat /etc/os-release | grep ^ID= | cut -d '\"' -f2")


def get_os_version():
    return get_command_output_string("cat /etc/os-release | grep VERSION_ID | cut -d '\"' -f2")


def get_glibc_version():
    return get_command_output_string("ldd --version | grep -i libc | awk '{print $NF}'")
    

def get_cpu_vendor():
    return get_command_output_string("lscpu | grep 'Vendor ID:' | awk '{print $3}'")


def is_cpu_amd():
    vendor_id = get_cpu_vendor()
    return vendor_id.strip() == "AuthenticAMD"


def is_cpu_intel():
    vendor_id = get_cpu_vendor()
    return vendor_id.strip() == "GenuineIntel"


def get_socket_count():
    return get_command_output_int("lscpu | grep 'Socket(s)' | awk '{print $2}'")


def get_numa_node_min_mem_GiB():
    if is_numactl_installed(False):
        return get_command_output_float("numactl -H | grep size: | awk '{print $4}' | sort -n | head -1") / 1024
    else:
        print("numactl must be installed for get_numa_node_min_mem_GiB")
        return -1


def get_numa_node_max_mem_GiB():
    if is_numactl_installed(False):
        return get_command_output_float("numactl -H | grep size: | awk '{print $4}' | sort -n | tail -1") / 1024
    else:
        print("numactl must be installed for get_numa_node_min_mem_GiB")
        return -1


def get_physical_cores_per_socket():
    return get_command_output_int("lscpu | grep 'Core(s) per socket' | awk '{print $4}'")


def get_physical_cores_total():
    return get_socket_count() * get_physical_cores_per_socket()


def get_physical_cores_per_numa_node():
    return get_physical_cores_total() / get_numa_node_count()


def get_threads_per_core():
    return get_command_output_int("lscpu | grep 'Thread(s) per core:' | awk '{print $4}'")


def get_hardware_threads_total():
    return get_physical_cores_total() * get_threads_per_core()


def get_mem_GiB():
    return get_command_output_int("free -g | grep 'Mem:' | awk '{print $2}'")


def get_mem_free_GiB():
    return get_command_output_int("free -g | grep 'Mem:' | awk '{print $4}'")


def get_cpu_family():
    return get_command_output_string("lscpu | grep 'CPU family:' | awk '{print $3}'")


def get_cpu_model():
    return get_command_output_string("lscpu | grep 'Model:' | awk '{print $2}'")


def get_cpu_arch():
    if is_cpu_bergamo():
        result = 'bergamo'
    elif is_cpu_genoa():
        result = 'genoa'
    elif is_cpu_milanx():
        result = 'milanx'
    elif is_cpu_milan():
        result = 'milan'
    elif is_cpu_rome():
        result = 'rome'
    elif is_cpu_naples():
        result = 'naples'
    elif is_cpu_ryzen():
        result = 'ryzen'
    elif is_cpu_ryzen_embedded():
        result = 'ryzen_embedded'
    elif is_cpu_amd_embedded():
        result = 'amd_embedded'
    elif is_cpu_threadripper():
        result = 'threadripper'
    elif is_cpu_amd():
        result = 'amd'
    elif is_cpu_intel():
        result = 'intel'
    else:
        result = 'unknown'
    return result


def get_cache_l1d_kb():
    l1d = get_command_output_string("lscpu | grep 'L1d cache:' | awk '{print $3}'")
    unit = get_command_output_string("lscpu | grep 'L1d cache:' | awk '{print $4}'")
    if unit == "MiB":
        l1d = get_command_output_string("cat /sys/devices/system/cpu/cpu0/cache/index0/size")
    l1d_kb = int(l1d[0: (len(l1d) - 1)])
    return l1d_kb


def get_cache_l1i_kb():
    l1i = get_command_output_string("lscpu | grep 'L1i cache:' | awk '{print $3}'")
    unit = get_command_output_string("lscpu | grep 'L1i cache:' | awk '{print $4}'")
    if unit == "MiB":
        l1i = get_command_output_string("cat /sys/devices/system/cpu/cpu0/cache/index1/size")
    l1i_kb = int(l1i[0: (len(l1i) - 1)])
    return l1i_kb


def get_cache_l2_kb():
    l2 = get_command_output_string("lscpu | grep 'L2 cache:' | awk '{print $3}'")
    unit = get_command_output_string("lscpu | grep 'L2 cache:' | awk '{print $4}'")
    if unit == "MiB":
        l2 = get_command_output_string("cat /sys/devices/system/cpu/cpu0/cache/index2/size")
    l2_kb = int(l2[0: (len(l2) - 1)])
    return l2_kb


def get_cache_l3_chip_kb():
    l3 = get_command_output_string("getconf LEVEL3_CACHE_SIZE")
    l3_kb = int(l3) / 1024
    return l3_kb


def get_cache_l3_chip_mb():
    l3 = get_command_output_string("getconf LEVEL3_CACHE_SIZE")
    l3_kb = int(l3) / 1048576
    return l3_kb


def get_nbr_of_l3():
    nbr_of_l3 = get_command_output_string(f'{LSTOPO_PATH} --of console | grep -i "L3 L#" | wc -l')
    nbr_of_l3 = int(nbr_of_l3)
    return nbr_of_l3


def get_physical_cores_per_ccx():
    nbr_of_l3 = int(get_command_output_string(f'{LSTOPO_PATH} --of console | grep -i "L3 L#" | wc -l'))
    nbr_of_l2 = int(get_command_output_string(f'{LSTOPO_PATH} --of console | grep -i "L2 L#" | wc -l'))
    return round( nbr_of_l2 / nbr_of_l3 )


def is_smt_enabled():
    result = False
    if get_threads_per_core() > 1:
        result = True
    return result


def is_cpu_bergamo():
    try:
        cpu_model = int(get_cpu_model())
    except ValueError:
        cpu_model = -1
    return is_cpu_amd() and get_cpu_family() == '25' and (cpu_model in [160])


def is_cpu_genoa():
    try:
        cpu_model = int(get_cpu_model())
    except ValueError:
        cpu_model = -1
    return is_cpu_amd() and get_cpu_family() == '25' and (cpu_model in [16, 17])


def is_cpu_milan():
    try:
        cpu_model = int(get_cpu_model())
    except ValueError:
        cpu_model = -1
    return is_cpu_amd() and get_cpu_family() == '25' and 0 <= cpu_model < 8


def is_cpu_milanx():
    return is_cpu_milan and (get_cache_l3_chip_mb() > 256)


def is_cpu_naples():
    try:
        cpu_model = int(get_cpu_model())
    except ValueError:
        cpu_model = -1
    return is_cpu_amd() and get_cpu_family() == '23' and 0 <= cpu_model < 8


def is_cpu_rome():
    try:
        cpu_model = int(get_cpu_model())
    except ValueError:
        cpu_model = -1
    return is_cpu_amd() and get_cpu_family() == '23' and 48 <= cpu_model < 56


def is_avx512_supported():
    try:
        result = get_command_output_string("lscpu | grep 'avx512'")
    except:
        result = ""
    if result:
        print('AVX-512 is supported.')
        return True
    else:
        print('AVX-512 is NOT supported.')
        return False

def get_cpu_model_name():
    if is_cpu_ryzen_embedded() or is_cpu_ryzen():
        result = get_command_output_string("lscpu | grep 'Model name:' | awk '{print $6}'")
        result = result.lower()
        print("The Ryzen Embedded model number is " + result)
    elif is_cpu_rome():
        result = get_command_output_string("lscpu | grep 'Model name:' | awk '{print $5}'")
        if not result[0].isdigit():
            result = "Rome" + str(get_physical_cores_per_socket())
        print("The Rome model number is " + result)
    elif is_cpu_milan():
        if is_cpu_milanx():
            result = get_command_output_string("lscpu | grep 'Model name:' | awk '{print $5}'")
            if result not in MILANX_MODELS:
                result = "Milanx" + str(get_physical_cores_per_socket())
            print("The Milan-X model number is " + result)
        else:
            result = get_command_output_string("lscpu | grep 'Model name:' | awk '{print $5}'")
            if not result[0].isdigit():
                result = "Milan" + str(get_physical_cores_per_socket())
            print("The Milan model number is " + result)
    elif is_cpu_genoa():
        result = get_command_output_string("lscpu | grep 'Model name:' | awk '{print $5}'")
        if not result[0].isdigit():
            result = "Genoa" + str(get_physical_cores_per_socket())
        print("The Genoa model number is " + result)
    elif is_cpu_bergamo():
        result = get_command_output_string("lscpu | grep 'Model name:' | awk '{print $5}'")
        if not result[0].isdigit():
            result = "Bergamo" + str(get_physical_cores_per_socket())
        print("The Bergamo model number is " + result)        
    elif is_cpu_intel():
        result = "Intel" + str(get_physical_cores_per_socket())
    else:
        result = get_command_output_string("lscpu | grep 'Model name:' | awk '{print $5}'")
        print("The (unknown architecture) model number is " + result)
    return result


def get_cpu_name():
    return get_command_output_string("lscpu | grep 'Model name:' | awk '{print $4}'")


def is_cpu_ryzen():
    result = False
    if is_cpu_amd():
        cpu_name = get_cpu_name()
        if cpu_name.lower() == "ryzen":
            result = True
    return result


def is_cpu_threadripper():
    result = False
    if is_cpu_amd():
        cpu_threadripper = get_command_output_string("lscpu | grep 'Model name:' | awk '{print $5}'")
        if cpu_threadripper.lower() == "threadripper":
            result = True
    return result


def is_cpu_amd_embedded():
    result = False
    if is_cpu_amd():
        cpu_name = get_cpu_name()
        if cpu_name.lower() == "embedded":
            result = True
    return result


def is_cpu_ryzen_embedded():
    result = False
    if is_cpu_ryzen():
        is_embedded = get_command_output_string("lscpu | grep 'Model name:' | awk '{print $5}'")
        if is_embedded.lower() == "embedded":
            result = True
    return result


def get_cpu_type():
    if is_cpu_threadripper():
        return "threadripper"
    if is_cpu_ryzen_embedded():
        return "ryzen_embedded"
    if is_cpu_amd_embedded():
        return "amd_embedded"
    if is_cpu_ryzen():
        return "ryzen"
    if is_cpu_naples() or is_cpu_rome() or is_cpu_milan():
        return "epyc"
    return "unknown"


def dump_all_sys_info():
    print("sys_info version: " + __version__)
    if is_numactl_installed(False):
        print("numactl is installed.")
    else:
        print("numactl is NOT installed.")
    numa_node_count = get_numa_node_count()
    print("The NUMA node count is: " + str(numa_node_count))
    cpu_vendor = get_cpu_vendor()
    print("The CPU vendor is: " + cpu_vendor)
    if is_cpu_amd():
        print("CPU is AMD")
    else:
        print("CPU is NOT AMD")
    socket_count = get_socket_count()
    print("The socket count is: " + str(socket_count))
    physical_cores_per_socket = get_physical_cores_per_socket()
    print("Physical cores per socket: " + str(physical_cores_per_socket))
    physical_cores = get_physical_cores_total()
    print("Total physical cores: " + str(physical_cores))
    if is_smt_enabled():
        print("SMT is enabled.")
    else:
        print("SMT is disabled.")
    print("Total hardware threads: " + str(get_hardware_threads_total()))
    mem_GiB = get_mem_GiB()
    print("Total system memory (GiB): " + str(mem_GiB))
    print("The CPU family is: " + get_cpu_family())
    print("The CPU model is: " + get_cpu_model())
    print("L1d (kB): " + str(get_cache_l1d_kb()))
    print("L1i (kB): " + str(get_cache_l1i_kb()))
    print("L2 (kB): " + str(get_cache_l2_kb()))
    print("L3 (kB): " + str(get_cache_l3_chip_kb()))
    print("The minimum NUMA node memory (GiB): " + str(get_numa_node_min_mem_GiB()))
    print("The maximum NUMA node memory (GiB): " + str(get_numa_node_max_mem_GiB()))
    print("The CPU model name is: " + get_cpu_model_name())
    if is_cpu_naples():
        print("The CPU is Naples.")
    elif is_cpu_rome():
        print("The CPU is Rome.")
    else:
        print("The CPU is neither Rome nor Naples.")


def get_hardware_numa_node_count_total():
    return get_command_output_int(f'{LSTOPO_PATH} --of console | grep "NUMANode" | wc -l')


def get_hardware_numa_node_count():
    return get_hardware_numa_node_count_total() / get_socket_count()


def get_cores_per_hardware_numa_node():
    physical_cores_per_socket = get_physical_cores_per_socket()
    hardware_numa_nodes = get_hardware_numa_node_count()
    if hardware_numa_nodes != 0:
        return physical_cores_per_socket / hardware_numa_nodes
    else:
        return physical_cores_per_socket


def get_gomp_cpu_affinity():
    return os.getenv("GOMP_CPU_AFFINITY")


def get_gomp_cpu_affinity_list(a_str):
    gomp_cpu_affinity = get_gomp_cpu_affinity()
    if gomp_cpu_affinity == "":
        return []
    else:
        return parse_gomp_cpu_affinity(gomp_cpu_affinity)


def parse_gomp_cpu_affinity_to_list(astr_gomp_cpu_affinity):
    core_list = []
    # Split string at spaces and store in list:
    gomp_cpu_affinity_list = astr_gomp_cpu_affinity.split(" ")
    # Split string at commas and store in list:
    gomp_cpu_affinity_list = astr_gomp_cpu_affinity.split(",")
    # Now we need to step through each element and build the core list:
    for element in gomp_cpu_affinity_list:
        #print("Element = " + element)
        if "-" in element:
            step = 1
            #print('We have encountered a range. Look for step:')
            if ":" in element:
                #print('Extract the step:')
                step = int(element.split(":")[1])
                # Extract the range:
                element_range = element.split(":")[0]
            else:
                element_range = element
                element_stride = 1            # add each core in range to list:
                #print(f'No step found. Range element = {element_range}')
            range_start, range_end = element_range.split("-")
            #print(f'range_start, range_end, step = {range_start}, {range_end}, {step}')
            for core in range(int(range_start), int(range_end) + 1, step):
                #print(f'core = {core}')
                core_list.append(core)
        else:
            # Add the element to the core list:
            core_list.append(int(element))
    core_list.sort()
    #print(core_list)
    return core_list


def get_ccx_total():
    return get_nbr_of_l3()


def get_ccx_per_numa_node():
    return round(get_ccx_total() / get_numa_node_count())


def get_ccx_per_socket():
    return round(get_ccx_total() / get_socket_count())


def get_ccd_per_socket():
    if is_cpu_milan() or is_cpu_genoa():
        # CCD count = CCX count:
        return get_ccx_per_socket()
    else:
        # Each CCD has two CCXs:
        return round(get_ccx_per_socket() / 2)
