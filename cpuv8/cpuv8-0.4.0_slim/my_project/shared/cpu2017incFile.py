#!/usr/bin/env python3

import random
import sys
import os
import datetime, time
import platform
from . import sys_info as sysinfo
from . import epyc_infoA8 as epyc_info

########################################################################
#                                                                      #
# Licensed per Software License Clickwrap (SPPO).PDF document          #
#                                                                      #
# Copyright 2018-2020 Advanced Micro Devices                           #
#                                                                      #
# PURPOSE: Defines the class for CPU2017 include file generation.      #
#                                                                      #
# VERSION: 1.0.0                                                       #
#                                                                      #
########################################################################

__version__ = "1.0.1"

class cCpu2017incFile(object):
    # Constants:
    EOL = "\n"
    EOLx2 = EOL + EOL
    HASH_LINE = 80 * '#' + EOL
    HASH_LINEx2 = HASH_LINE + HASH_LINE

    # field variables
    notes_compiler = "Set notes_compiler in ini file."
    is_speed = False
    notes_os = "Set notes_os in ini file."
    notes_submit = "Set notes_submit in ini file."

    inc_file_date = "Set inc_file_date file date in binary package inc file."
    inc_file_name = "Set inc_file_name in binary package inc file."
    inc_file_path = "config"

    cpu_model_info = epyc_info.CpuModels()

    # How many sockets does your test system have? (Naples supports 1 or 2)
    number_of_sockets = 2

    __number_of_physical_cores_per_socket = 1
    @property
    def number_of_physical_cores_per_socket(self):
        return self.__number_of_physical_cores_per_socket

    @number_of_physical_cores_per_socket.setter
    def number_of_physical_cores_per_socket(self, value):
        self.__number_of_physical_cores_per_socket = value
        self.calculate_cores()

    number_of_physical_cores_total = 0
    number_of_logical_cores_total = 0

    physical_cores_div_2_affinity = []
    physical_cores_div_2_benchmarks = ""
    physical_cores_div_2 = 0
    physical_cores_div_4_benchmarks = ""
    physical_cores_div_4_affinity = []
    physical_cores_div_4 = 0

    GiB_per_logical_core = 0

    rate_copies = 0
    affinity_type = "normal"
    cores_affinity_list = []

    smt_enabled = True

    auto_bind = True

    license_number = ""

    tester = ""
    test_sponsor = ""
    test_date = ""

    hw_vendor = ""
    hw_disk = ""
    hw_memory000 = ""
    hw_memory001 = ""
    hw_memory002 = ""

    hw_model000 = ""
    hw_model001 = ""

    hw_other = ""

    fw_bios = ""

    prepared_by = ""

    sw_other000 = ""
    sw_other001 = ""

    sw_os000 = ""
    sw_os001 = ""
    sw_os002 = ""

    sw_state = ""

    notes = ""

    notes_plat = ""

    int_only = ""
    fp_only = ""

    enable_mitigation_notes = True
    mitigation_notes = "Set the mitigation notes in the ini file (notes_198 - notes_210)."

    custom_fields = ""

    # How many gibibytes of memory are in the system?
    memory_GiB = 512

    # What is the rated frequency (MT/s) of the DDR4 memory in your system?
    # (2133, 2400, 2667)
    memory_MTs = 2667

    # At what speed is your DDR4 memory running? For example, its rated frequency
    # might be 2667 MT/s, but it is running at a down-clocked speed of 2400.
    # (2133, 2400, 2667)
    memory_MTs_actual = 2667

    # Specify the number of DDR4 memory sticks in your SUT:
    memory_stick_count = 16

    # What is your DDR4 memory rank? (1 or 2)
    memory_rank = 2

    # What is the DDR4 device organization bit width? (4 or 8)
    ddr4_bus_width = 4

    # What is the DDR4 speed grade (CL-tRCD-tRP)?
    # J = 10-10-10
    # K = 11-11-11
    # L = 12-12-12
    # M = 13-13-13
    # N = 14-14-14
    # P = 15-15-15
    # R = 16-16-16
    # U = 18-18-18
    # T = 17-17-17
    # V = 19-19-19
    ddr4_speed_grade = "V"

    # What is the DDR4 module type?
    mem_module_type = "R"

    ################################################################################
    # Hardware information
    ################################################################################
    hw_avail = ""
    sw_avail = ""
    hw_cpu_name = ""
    hw_cpu_max_mhz = ""
    hw_cpu_nominal_mhz = ""
    hw_nchips = ""
    hw_ncores = ""
    hw_ncpuorder = ""
    hw_nthreadspercore = ""
    hw_ocache = ""
    hw_pcache = ""
    hw_scache = ""
    hw_tcache = ""
    sw_base_ptrsize = ""
    sw_peak_ptrsize = ""
    sw_compiler000 = ""
    sw_compiler001 = ""
    sw_compiler002 = ""
    sw_file = ""

    cpu_info = epyc_info.CpuInfo("9654", True, 0)

    def __init__(self, a_model_number, a_number_of_sockets, a_smt_enabled, a_ctdp=0, a_memory_mts_max=0):
        self.cpu_info.smt_enabled = a_smt_enabled
        self.cpu_info.ctdp = a_ctdp
        self.cpu_info.memory_mts_max = a_memory_mts_max
        self.cpu_info.model_number = a_model_number
        self.smt_enabled = a_smt_enabled
        self.number_of_sockets = a_number_of_sockets
        self.number_of_physical_cores_per_socket = self.cpu_info.physical_core_count

    def add_physical_cores_div_2_benchmarks(self, a_benchmark):
        if self.physical_cores_div_2_benchmarks == "":
            self.physical_cores_div_2_benchmarks = a_benchmark
        else:
            a_benchmark += ','
            self.physical_cores_div_2_benchmarks += a_benchmark

    def add_physical_cores_div_4_benchmarks(self, a_benchmark):
        if self.physical_cores_div_4_benchmarks == "":
            self.physical_cores_div_4_benchmarks = a_benchmark
        else:
            a_benchmark += ','
            self.physical_cores_div_4_benchmarks += a_benchmark

    def create_inc_file_header(self):
        t = datetime.datetime.now()
        generation_date_time = t.strftime('%B %d, %Y / %T')
        inc_file_header = self.HASH_LINEx2 + "# File name: " + self.inc_file_name + self.EOL + \
                      "# File generation code date: " + self.inc_file_date + self.EOL + \
                      "# File generation date/time: " + generation_date_time + self.EOL + \
                      "#\n# This file is automatically generated during a SPEC CPU2017 run." + self.EOL +\
                      "#\n# To modify inc file generation, please consult the readme file or the run \n# script." + \
                      self.EOL + self.HASH_LINEx2
        return inc_file_header

    def create_report_header(self):
        result = self.HASH_LINEx2 + "# The remainder of this file defines CPU2017 report parameters." + self.EOL + \
                 self.HASH_LINEx2
        result += self.HASH_LINE + "# SPEC CPU 2017 report header" + self.EOL + self.HASH_LINE
        result += "license_num              =" + str(self.license_number) + " # (Your SPEC license number)" + self.EOL
        result += "tester                   =" + self.tester + self.EOL
        if self.test_sponsor != "":
            result += "test_sponsor             =" + self.test_sponsor + self.EOL
        result += "hw_vendor                =" + self.hw_vendor + self.EOL
        result += "hw_model000              =" + self.hw_model000 + self.EOL
        if self.hw_model001 != "":
            result += "hw_model001              =" + self.hw_model001 + self.EOL
        else:
            result += "hw_model001              =AMD EPYC " + self.cpu_info.model_number.upper() + self.EOL
        result += "#--------- If you install new compilers, edit this section --------------------" + self.EOL
        if self.sw_compiler000 != "":
            result += "sw_compiler000           =" + self.sw_compiler000 + self.EOL
        if self.sw_compiler001 != "":
            result += "sw_compiler001           =" + self.sw_compiler001 + self.EOL
        if self.sw_compiler002 != "":
            result += "sw_compiler002           =" + self.sw_compiler002 + self.EOL
        result += self.HASH_LINE
        return result

    def create_hardware_section(self):
        result = self.HASH_LINE + "# Hardware, firmware and software information" + self.EOL + self.HASH_LINE
        if self.hw_avail:
            result += "hw_avail                 =" + self.hw_avail + self.EOL
        else:
            result += "hw_avail                 =mmm-yyyy              # ex.: Sep-2018" + self.EOL
        if self.sw_avail:
            result += "sw_avail                 =" + self.sw_avail + self.EOL
        else:
            result += "sw_avail                 =mmm-yyyy              # ex.: Sep-2018" + self.EOL
        if self.hw_cpu_name == "":
            result += "hw_cpu_name              =AMD EPYC " + self.cpu_info.model_number.upper() + self.EOL
        else:
            result += "hw_cpu_name              =" + self.hw_cpu_name + self.EOL
        if self.hw_cpu_nominal_mhz == "":
            result += "hw_cpu_nominal_mhz       =" + str(self.cpu_info.clock_speed_nominal) + self.EOL
        else:
            result += "hw_cpu_nominal_mhz       =" + self.hw_cpu_nominal_mhz + self.EOL
        if self.hw_cpu_max_mhz == "":
            result += "hw_cpu_max_mhz           =" + str(self.cpu_info.clock_speed_boost_max) + self.EOL
        else:
            result += "hw_cpu_max_mhz           =" + self.hw_cpu_max_mhz + self.EOL
        if self.hw_ncores == "":
            result += "hw_ncores                =" + str(self.number_of_physical_cores_total) + self.EOL
        else:
            result += "hw_ncores                =" + self.hw_ncores + self.EOL
        if self.hw_nthreadspercore != "":
            result += "hw_nthreadspercore       =" + self.hw_nthreadspercore + self.EOL
        elif self.smt_enabled:
            result += "hw_nthreadspercore       =2" + self.EOL
        else:
            result += "hw_nthreadspercore       =1" + self.EOL
        if self.hw_ncpuorder != "":
            result += "hw_ncpuorder             =" + self.hw_ncpuorder + self.EOL
        elif self.number_of_sockets == 1:
            result += "hw_ncpuorder             =1 chip" + self.EOL
        else:
            result += "hw_ncpuorder             =1,2 chips" + self.EOL
        result += self.EOL
        if self.hw_other == "":
            result += 'hw_other                 =None                  # Other perf-relevant hw, or "None"' + self.EOL
        else:
            result += "hw_other                 =" + self.hw_other + self.EOL
        result += "fw_bios                  =" + self.fw_bios + self.EOL
        if self.sw_base_ptrsize == "":
            result += "sw_base_ptrsize          =64-bit" + self.EOL
        else:
            result += "sw_base_ptrsize          =" + self.sw_base_ptrsize + self.EOL
        if self.hw_pcache == "":
            result += "hw_pcache                =" + str(self.cpu_info.l1i_kib) + " KB I + " + str(self.cpu_info.l1d_kib) + " KB D on chip per core" + self.EOL
        else:
            result += "hw_pcache                =" + self.hw_pcache + self.EOL
        if self.hw_scache == "":
            if self.cpu_info.l2_kib < 1024:
                result += "hw_scache                =" + str(self.cpu_info.l2_kib) + " KB I+D on chip per core" + self.EOL
            else:
                if self.cpu_info.l2_kib == 1024:
                    l2 = "1"
                else:
                    l2 = str(self.cpu_info.l2_kib / 1024)
                result += "hw_scache                =" + l2 + " MB I+D on chip per core" + self.EOL                
        else:
            result += "hw_scache                =" + self.hw_scache + self.EOL
        if self.hw_tcache == "":
            result += "hw_tcache                =" + self.cpu_info.l3_mb_per_core + self.EOL
        else:
            result += "hw_tcache                =" + self.hw_tcache + self.EOL
        if self.hw_ocache == "":
            result += "hw_ocache                =None" + self.EOL
        else:
            result += "hw_ocache                =" + self.hw_ocache + self.EOL
        if self.sw_other000 != "":
            result += "sw_other000              =" + self.sw_other000 + self.EOL
            if self.sw_other001 != "":
                result += "sw_other001              =" + self.sw_other001 + self.EOL
        return result


    def create_general_notes_section(self):
        result = self.HASH_LINE + "# Notes" + self.EOL + self.HASH_LINE + self.EOLx2
        result += self.notes + self.EOL
        if self.enable_mitigation_notes:
            result += self.mitigation_notes
        return result

    def calculate_cores(self):
        self.number_of_physical_cores_total = self.number_of_sockets * self.number_of_physical_cores_per_socket
        if self.smt_enabled:
            self.number_of_logical_cores_total = 2 * self.number_of_physical_cores_total
        else:
            self.number_of_logical_cores_total = self.number_of_physical_cores_total
        # Calculate the amount of memory per logical core:
        self.GiB_per_logical_core = self.memory_GiB / self.number_of_logical_cores_total
        self.physical_cores_div_4 = self.number_of_physical_cores_total / 4
        self.physical_cores_div_4_affinity = range(0, self.number_of_physical_cores_total, 4)
        self.physical_cores_div_4_benchmarks = ""
        self.physical_cores_div_2 = self.number_of_physical_cores_total / 2
        self.physical_cores_div_2_affinity = range(0, self.number_of_physical_cores_total, 2)
        self.physical_cores_div_2_benchmarks = ""

    # create_macro_section(self): This is a virtual method which should be
    # extended in the package file.
    def create_macro_section(self):
        self.calculate_cores()
        result = self.HASH_LINEx2 + "# The following macros are generated for use in the cfg file." + \
                 self.EOL + self.HASH_LINEx2 + self.EOL
        result += "%define logical_core_count " + str(self.number_of_logical_cores_total) + self.EOL
        result += "%define physical_core_count " + str(self.number_of_physical_cores_total) + self.EOLx2
        result += self.HASH_LINE
        return result

    def get_benchmark_string(self, a_benchmark_list = []):
        result_list = []
        if a_benchmark_list == []:
            return ""
        # Rate benchmarks
        if 500 in a_benchmark_list:
            result_list.append('500.perlbench_r')
        if 502 in a_benchmark_list:
            result_list.append('502.gcc_r')
        if 503 in a_benchmark_list:
            result_list.append('503.bwaves_r')
        if 505 in a_benchmark_list:
            result_list.append('505.mcf_r')
        if 507 in a_benchmark_list:
            result_list.append('507.cactuBSSN_r')
        if 508 in a_benchmark_list:
            result_list.append('508.namd_r')
        if 510 in a_benchmark_list:
            result_list.append('510.parest_r')
        if 511 in a_benchmark_list:
            result_list.append('511.povray_r')
        if 519 in a_benchmark_list:
            result_list.append('519.lbm_r')
        if 520 in a_benchmark_list:
            result_list.append('520.omnetpp_r')
        if 521 in a_benchmark_list:
            result_list.append('521.wrf_r')
        if 523 in a_benchmark_list:
            result_list.append('523.xalancbmk_r')
        if 525 in a_benchmark_list:
            result_list.append('525.x264_r')
        if 526 in a_benchmark_list:
            result_list.append('526.blender_r')
        if 527 in a_benchmark_list:
            result_list.append('527.cam4_r')
        if 531 in a_benchmark_list:
            result_list.append('531.deepsjeng_r')
        if 538 in a_benchmark_list:
            result_list.append('538.imagick_r')
        if 541 in a_benchmark_list:
            result_list.append('541.leela_r')
        if 544 in a_benchmark_list:
            result_list.append('544.nab_r')
        if 548 in a_benchmark_list:
            result_list.append('548.exchange2_r')
        if 549 in a_benchmark_list:
            result_list.append('549.fotonik3d_r')
        if 554 in a_benchmark_list:
            result_list.append('554.roms_r')
        if 557 in a_benchmark_list:
            result_list.append('557.xz_r')
        # Speed benchmarks    
        if 600 in a_benchmark_list:
            result_list.append('600.perlbench_s')
        if 602 in a_benchmark_list:
            result_list.append('602.gcc_s')
        if 603 in a_benchmark_list:
            result_list.append('603.bwaves_s')
        if 605 in a_benchmark_list:
            result_list.append('605.mcf_s')
        if 607 in a_benchmark_list:
            result_list.append('607.cactuBSSN_s')
        if 619 in a_benchmark_list:
            result_list.append('619.lbm_s')
        if 620 in a_benchmark_list:
            result_list.append('620.omnetpp_s')
        if 621 in a_benchmark_list:
            result_list.append('621.wrf_s')
        if 623 in a_benchmark_list:
            result_list.append('623.xalancbmk_s')
        if 625 in a_benchmark_list:
            result_list.append('625.x264_s')
        if 627 in a_benchmark_list:
            result_list.append('627.cam4_s')
        if 628 in a_benchmark_list:
            result_list.append('628.pop2_s')
        if 631 in a_benchmark_list:
            result_list.append('631.deepsjeng_s')
        if 638 in a_benchmark_list:
            result_list.append('638.imagick_s')
        if 641 in a_benchmark_list:
            result_list.append('641.leela_s')
        if 644 in a_benchmark_list:
            result_list.append('644.nab_s')
        if 648 in a_benchmark_list:
            result_list.append('648.exchange2_s')
        if 649 in a_benchmark_list:
            result_list.append('649.fotonik3d_s')
        if 654 in a_benchmark_list:
            result_list.append('654.roms_s')
        if 657 in a_benchmark_list:
            result_list.append('657.xz_s')
        result = ",".join(result_list)
        return result

    def get_memory_description_string(self):
        if self.hw_memory000 == "":
            memoryStickSize = self.memory_GiB / self.memory_stick_count
            result = "hw_memory000             =" + str(self.memory_GiB) + " GB (" + str(self.memory_stick_count) + \
                     " x " + str(memoryStickSize) + " GB " + str(self.memory_rank) + "Rx" + \
                     str(self.ddr4_bus_width) + "PC4-" + str(self.memory_MTs) + self.ddr4_speed_grade + "-" + \
                     self.mem_module_type + ")" + self.EOL
        else:
            result = "hw_memory000             =" + self.hw_memory000 + self.EOL
        if self.hw_memory001 == "":
            if self.memory_MTs == self.memory_MTs_actual:
                result += "hw_memory001             =" + self.EOL
            else:
                result +=  "hw_memory001          =running at" + self.memory_MTs_actual + self.EOL
        else:
            result += "hw_memory001             =" + self.hw_memory001 + self.EOL
        if self.hw_memory002 == "":
            # The following field must be made blank or sysinfo will output placeholder info in it:
            result += "hw_memory002             =" + self.EOL
        else:
            result += "hw_memory002             =" + self.hw_memory002 + self.EOL
        return result

    # a_list_of_benchmarks should be a string list of benchmarks:
    def get_default_base_peak_copies_block(self, a_list_of_benchmarks, a_copy_affinity):
        copy_count = len(a_copy_affinity)
        result = self.HASH_LINE
        if ('intrate' in a_list_of_benchmarks) or ('fprate' in a_list_of_benchmarks) or ('default' in a_list_of_benchmarks):
            result += "# " + a_list_of_benchmarks + " copy counts:" + self.EOL
            result += a_list_of_benchmarks + ":" + self.EOL
        else:
            result += "# peak copy counts: " + str(copy_count) + self.EOL
            result += a_list_of_benchmarks + "=peak:" + self.EOL
        result += "copies                  = " + str(copy_count) + self.EOL
        result += self.create_bind_commands(a_copy_affinity)
        result += self.HASH_LINE
        return result

    # a_list_of_benchmarks should be a string list of benchmarks:
    def get_base_peak_threads_block(self, a_list_of_benchmarks, a_thread_count, a_thread_affinity):
        result = self.HASH_LINE
        if ('intspeed' in a_list_of_benchmarks) or ('fpspeed' in a_list_of_benchmarks):
            result += "# " + a_list_of_benchmarks + " base thread counts:" + self.EOL
            result += a_list_of_benchmarks + "=base:" + self.EOL
        else:
            result += "# peak thread counts: " + str(a_thread_count) + self.EOL
            result += a_list_of_benchmarks + "=peak:" + self.EOL
        result += "threads                  = " + str(a_thread_count) + self.EOL
        if a_thread_count == 1:
            result += "ENV_GOMP_CPU_AFFINITY    = 0" + self.EOL
            result += "bind0                    = numactl --physcpubind=0" + self.EOL
        elif a_thread_affinity == "normal_physical":
            result += "ENV_GOMP_CPU_AFFINITY    = 0-" + str(a_thread_count - 1) + self.EOL
            result += "bind0                    = numactl --physcpubind=0-" + str(a_thread_count - 1) + self.EOL
        elif a_thread_affinity == "normal_logical":
            result += "ENV_GOMP_CPU_AFFINITY    = 0-" + str(a_thread_count - 1) + self.EOL
            result += "bind0                    = numactl --physcpubind=0-" + str(a_thread_count - 1) + self.EOL
        elif a_thread_affinity == "local_logical":
            # in this case, we have to pair the SMT logical cores:
            smt_start = a_thread_count / 2
            core_sequence = ""
            for thread_number in range(0, smt_start):
                core_sequence += str(thread_number) + " " + str(thread_number + smt_start)
                if thread_number < smt_start - 1:
                    core_sequence += " "
            result += "ENV_GOMP_CPU_AFFINITY    = " + core_sequence + self.EOL
            result += "bind0                    = numactl --physcpubind=0-" + str(a_thread_count - 1) + self.EOL
        elif a_thread_affinity == "normal_physical_div_2":
            core_sequence = "0-" + str(a_thread_count - 1) + ':2'
            result += "ENV_GOMP_CPU_AFFINITY    = " + core_sequence + self.EOL
            result += "bind0                    = numactl --physcpubind=0-" + str(a_thread_count - 1) + self.EOL
        elif a_thread_affinity == "normal_physical_div_4":
            core_sequence = "0-" + str(a_thread_count - 1) + ':4'
            result += "ENV_GOMP_CPU_AFFINITY    = " + core_sequence + self.EOL
            result += "bind0                    = numactl --physcpubind=0-" + str(a_thread_count - 1) + self.EOL
        result += 'submit = echo "$command" > run.sh ; $BIND bash run.sh' + self.EOL
        result += self.HASH_LINE
        return result

    # a_list_of_benchmarks should be a string list of benchmarks:
    def get_default_threads_block(self, a_thread_count, a_thread_affinity):
        result = self.HASH_LINE
        result += "# default preENV thread settings:" + self.EOL
        result += "default:" + self.EOL
        result += "preENV_OMP_THREAD_LIMIT  = " + str(a_thread_count) + self.EOL
        if a_thread_count == 1:
            result += "preENV_GOMP_CPU_AFFINITY = 0" + self.EOL
        elif a_thread_affinity == "normal_physical":
            result += "preENV_GOMP_CPU_AFFINITY = 0-" + str(a_thread_count - 1) + self.EOL
        elif a_thread_affinity == "normal_logical":
            result += "preENV_GOMP_CPU_AFFINITY = 0-" + str(a_thread_count - 1) + self.EOL
        elif a_thread_affinity == "local_logical":
            # in this case, we have to pair the SMT logical cores:
            smt_start = a_thread_count / 2
            core_sequence = ""
            for thread_number in range(0, smt_start):
                core_sequence += str(thread_number) + " " + str(thread_number + smt_start)
                if thread_number < smt_start - 1:
                    core_sequence += " "
            result += "preENV_GOMP_CPU_AFFINITY    = " + core_sequence + self.EOL
        elif a_thread_affinity == "normal_physical_div_2":
            core_sequence = "0-" + str(a_thread_count - 1) + ':2'
            result += "preENV_GOMP_CPU_AFFINITY    = " + core_sequence + self.EOL
        elif a_thread_affinity == "normal_physical_div_4":
            core_sequence = "0-" + str(a_thread_count - 1) + ':4'
            result += "preENV_GOMP_CPU_AFFINITY    = " + core_sequence + self.EOL
        result += self.HASH_LINE
        return result

    def create_bind_commands(self, a_copy_affinity):
        result = "# Bind commands for assigning affinity:" + self.EOL
        bind_number = 0
        if self.auto_bind:
            for coreNumber in a_copy_affinity:
                result += "bind" + str(bind_number) + "            = numactl --localalloc --physcpubind=" + str(coreNumber) + self.EOL
                bind_number += 1
        elif self.cores_affinity_list != []:
            bind_number = 0
            for coreNumber in self.cores_affinity_list:
                result += "bind" + str(bind_number) + "            = numactl --localalloc --physcpubind=" + str(coreNumber) + self.EOL
                bind_number += 1
        else:
            for coreNumber in a_copy_affinity:
                result += "bind" + str(bind_number) + "            = numactl --localalloc --physcpubind=" + str(coreNumber) + self.EOL
                bind_number += 1
        result += 'submit = echo "$command" > run.sh ; $BIND bash run.sh' + self.EOL
        return result

    def create_notes_plat_fields(self):
        result = self.HASH_LINE + "# The following note fields describe platorm settings." + \
                 self.EOL + self.HASH_LINE
        if self.notes_plat:
            result += self.notes_plat + self.EOL
        else:
            result += "# No platform notes defined." + self.EOL
        #print(f'plat_fields = {result}')
        return result

    def create_custom_fields(self):
        result = self.HASH_LINE + "# The following are custom fields:" + self.EOL + self.HASH_LINE
        if self.custom_fields:
            result += self.custom_fields + self.EOL
        else:
            result += "# No custom fields defined." + self.EOL
        return result

    def create_int_fields(self):
        if self.int_only != "":
            result = self.HASH_LINE + "# The following fields must be set here for only Int benchmarks." + \
                     self.EOL + self.HASH_LINE
            if self.is_speed:
                result += 'intspeed:' + self.EOL
            else:
                result += 'intrate:' + self.EOL
            result += self.int_only + self.EOL
        return result

    def create_fp_fields(self):
        if self.fp_only != "":
            result = self.HASH_LINE + "# The following fields must be set here for FP benchmarks." + \
                     self.EOL + self.HASH_LINE
            if self.is_speed:
                result += 'fpspeed:' + self.EOL
            else:
                result += 'fprate:' + self.EOL
            result += self.fp_only + self.EOL
        return result

    def create_non_default_fields(self):
        result = self.HASH_LINE + "# The following fields must be set here or they will be overwritten by sysinfo." + \
                 self.EOL + self.HASH_LINE
        if self.is_speed:
            result += self.EOL + "intspeed,fpspeed:" + self.EOL
        else:
            result += self.EOL + "intrate,fprate:" + self.EOL            
        if self.hw_disk == "":
            result += "hw_disk                  =count size type, other perf-relevant info   " + \
                    "# ex: 1 x 1 TB SSD" + self.EOL
        else:
            result += "hw_disk                  =" + self.hw_disk + self.EOL
        result += self.get_memory_description_string() + self.EOL
        if self.hw_nchips == "":
            result += "hw_nchips                =" + str(self.number_of_sockets) + self.EOL
        else:
            result += "hw_nchips                =" + self.hw_nchips + self.EOL
        result += "prepared_by              =" + self.prepared_by + self.EOL
        if self.sw_file:
            result += "sw_file                  =" + self.sw_file + self.EOL
        else:
            result += "sw_file                  =FileSystem                                  " + \
                      "# ex1: ext4, ex2: ntfs" + self.EOL
        if self.sw_os000:
            result += "sw_os000                 =" + self.sw_os000 + self.EOL
        else:
            result += "sw_os000                 =OperatingSystemName Version                 " + \
                      "# ex: Ubuntu 16.04 LTS," + self.EOL
        if self.sw_os001:
            result += "sw_os001                 =" + self.sw_os001 + self.EOL
        else:
            result += "sw_os001                 =kernel version                              " + \
                      "# ex: Kernel 4.4.0-87-generic" + self.EOL
        if self.sw_os002:
            result += "sw_os002                 =" + self.sw_os002 + self.EOL
        if self.sw_state:
            result += "sw_state                 =" + self.sw_state + self.EOL
        else:
            result += "sw_state                 =RunLevel/target                             " + \
                      "# ex: Run level 3 (Full multiuser with network)" + self.EOL
        return result

    def close_inc_file(self):
        result = self.HASH_LINE + "# End of inc file" + self.EOL + self.HASH_LINE
        result += "# Switch back to the default block after the include file:" + self.EOLx2
        result += "default:" + self.EOL
        return result

    def run_checks(self):
        self.calculate_cores()
        if self.cpu_info.cpu_is_known:
            # Verify socket count:
            if (self.number_of_sockets > self.cpu_info.socket_count_max) or (self.number_of_sockets < 1):
                print('*** ERROR: You have specified an invalid number of CPU sockets: ' + \
                    str(self.number_of_sockets) + ", " + str(self.cpu_info.socket_count_max))
                quit()
            # Verify ctdp:
            if self.cpu_info.ctdp > self.cpu_info.tdp:
                print('*** WARNING: You specified a ctdp that exceeds the TDP: ' + str(self.cpu_info.ctdp) + ' vs ' + \
                    str(self.cpu_info.tdp))
                print('Be sure to add the ctdp documentation specified in Readme.amd1704na-rate_revX.txt')
                print('to amd1704-INVALID-platform-revX-Y.xml for result submissions.')
            # Verify that logical core value is correct:
            if (self.cpu_info.logical_core_count < self.cpu_info.physical_core_count) or \
               (self.cpu_info.logical_core_count <= 0):
                print('*** ERROR: Your logical core count is invalid ' + str(self.cpu_info.logical_core_count))
                quit()
            # Verify that memory amount per copy is good:
            lMemTotalGiB = sysinfo.get_mem_GiB()
            lTotalLogicalCores = self.cpu_info.logical_core_count * self.number_of_sockets
            print(f'Memory detected = {lMemTotalGiB} GiB')
            print(f'Logical core count = {lTotalLogicalCores}')
            lGiB_per_logical_core = lMemTotalGiB / lTotalLogicalCores
            print(f'Memory per logical core = {lGiB_per_logical_core} GiB')
            if lGiB_per_logical_core < 2:
                print('*** CRITICAL WARNING! You have less than the needed 2 GiB per logical core.')
            elif lGiB_per_logical_core < 3.6:
                print('*** WARNING: You have less than the recommended 4 GiB per logical core.')
            else:
                print('Memory capacity is good.')
        else:
            print('*** WARNING: Your CPU is not recognized.')

    def write_file(self):
        self.calculate_cores()
        self.run_checks()
        incFile = self.inc_file_path + "/" + self.inc_file_name
        f = open(incFile, "w+")
        f.write(self.create_inc_file_header() + self.EOL)
        f.write(self.create_macro_section() + self.EOL)
        f.write(self.create_report_header() + self.EOL)
        f.write(self.create_hardware_section() + self.EOL)
        f.write(self.create_general_notes_section() + self.EOL)
        f.write(self.notes_submit + self.EOL)
        f.write(self.notes_os + self.EOL)
        f.write(self.notes_compiler + self.EOL)
        f.write(self.create_notes_plat_fields() + self.EOL)
        f.write(self.create_custom_fields() + self.EOL)
        f.write(self.create_int_fields() + self.EOL)
        f.write(self.create_fp_fields() + self.EOL)
        f.write(self.create_non_default_fields() + self.EOL)
        f.write(self.close_inc_file() + self.EOL)
        f.close()

########################################################################################################################
# End class cCpu2017incFile
########################################################################################################################
