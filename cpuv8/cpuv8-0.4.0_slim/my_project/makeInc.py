#!/usr/bin/env python3

from .shared.cpu2017incFile import cCpu2017incFile
from .shared import sys_info as sys_info

########################################################################
#                                                                      #
# Licensed per Software License Clickwrap (SPPO).PDF document          #
#                                                                      #
# Copyright 2018-2020 Advanced Micro Devices                           #
#                                                                      #
# PURPOSE: Generate the CPU2017 include file.                          #
#                                                                      #
# VERSION: 1.0.0                                                       #
#                                                                      #
########################################################################

class cCpu2017incFileRate(cCpu2017incFile):
    def __init__(self, amodel_number, aNumberOfSockets, aSmtEnabled, aCTdp=0, aMaxDdr4MHz=0):
        cCpu2017incFile.__init__(self, amodel_number, aNumberOfSockets, aSmtEnabled, a_ctdp=0, a_memory_mts_max=0)
        self.inc_file_name = "amd_rate_aocc400_genoa_A1.inc"
        self.inc_file_date = "September 23, 2022"

        # Calculate number of physical and logical cores:
        if self.smt_enabled:
            self.number_of_logical_cores_per_socket = 2 * self.number_of_physical_cores_per_socket
        else:
            self.number_of_logical_cores_per_socket = self.number_of_physical_cores_per_socket
        self.number_of_physical_cores_total = self.number_of_sockets * self.number_of_physical_cores_per_socket
        self.number_of_logical_cores_total = self.number_of_sockets * self.number_of_logical_cores_per_socket
        # Calculate the amount of memory per logical core:
        self.GiB_per_logical_core = self.memory_GiB / self.number_of_logical_cores_total

        # Map from symbolic quantities expressed in the counts_by_* section of the cpu_info.json file to actual values
        # Some of this ("<whatever>/n") could be generalized, but that's for later.
        if aNumberOfSockets == 1:
          self.quantities_map = {
              "logical_cores": range(0, self.number_of_logical_cores_total),
              "physical_cores": range(0, self.number_of_physical_cores_total),
              "physical/2": range(0, self.number_of_physical_cores_total, 1 if self.affinity_type.lower() == 'dell' else 2),
              "physical/4": range(0, self.number_of_physical_cores_total, 1 if self.affinity_type.lower() == 'dell' else 4),
              "10": range(1, 11),
              "8": range(1, 9),
              "6": range(1, 7),
              "5": range(1, 6),
              "4": range(1, 5),
              "3": range(1, 4),
              "2": range(1, 3),
              "1": [1]
          }
        else:
          self.quantities_map = {
              "logical_cores": range(0, self.number_of_logical_cores_total),
              "physical_cores": range(0, self.number_of_physical_cores_total),
              "physical/2": range(0, self.number_of_physical_cores_total, 1 if self.affinity_type.lower() == 'dell' else 2),
              "physical/4": range(0, self.number_of_physical_cores_total, 1 if self.affinity_type.lower() == 'dell' else 4),
              "10": [*range(1, 11)] + [*range(self.number_of_physical_cores_total,self.number_of_physical_cores_total + 11, 1)],
               "8": [*range(1, 9)] + [*range(self.number_of_physical_cores_total,self.number_of_physical_cores_total+9)],
               "6": [*range(1, 7)] + [*range(self.number_of_physical_cores_total,self.number_of_physical_cores_total+7)],
               "5": [*range(1, 6)] + [*range(self.number_of_physical_cores_total,self.number_of_physical_cores_total+6)],
               "4": [*range(1, 5)] + [*range(self.number_of_physical_cores_total,self.number_of_physical_cores_total+5)],
               "3": [*range(1, 4)] + [*range(self.number_of_physical_cores_total,self.number_of_physical_cores_total+4)],
               "2": [*range(1, 3)] + [*range(self.number_of_physical_cores_total,self.number_of_physical_cores_total+3)],
               "1": [1,self.number_of_physical_cores_total+1]
          }

    def detect_auto_bind(self):
        if (self.cores_affinity_list != []) or (self.rate_copies > 0):
            self.auto_bind = False
        else:
            self.auto_bind = True

    def create_macro_section(self):
        self.detect_auto_bind()
        result = self.HASH_LINEx2 + "# The following macros are generated for use in the cfg file." + self.EOL + self.HASH_LINEx2 + self.EOL
        result += "%define logical_core_count " + str(self.number_of_logical_cores_total) + self.EOL
        result += "%define physical_core_count " + str(self.number_of_physical_cores_total) + self.EOLx2
        result += self.HASH_LINE + "# The following inc blocks set the rate copy counts and affinity settings." + self.EOL
        result += "#" + self.EOL
        result += "# intrate benchmarks: 500.perlbench_r,502.gcc_r,505.mcf_r,520.omnetpp_r," + self.EOL
        result += "#   523.xalancbmk_r,525.x264_r,531.deepsjeng_r,541.leela_r,548.exchange2_r," + self.EOL
        result += "#   557.xz_r" + self.EOL
        result += "# fpspeed benchmarks: 503.bwaves_r,507.cactuBSSN_r,519.lbm_r,521.wrf_r," + self.EOL
        result += "#   527.cam4_r,538.imagick_r,544.nab_r,549.fotonik3d_r,554.roms_r" + self.EOL
        result += "#" + self.EOL

        if self.auto_bind:
            epyc_model_number = self.cpu_info.model_number.lower()
            cpu_type_and_size = f"{sys_info.get_cpu_type()}{int(sys_info.get_physical_cores_per_numa_node())}n"
            physical_cores_tag = f"{self.number_of_physical_cores_per_socket}p"
            logical_cores_tag = f"{self.number_of_logical_cores_per_socket}l"

            # First try by model name
            if epyc_model_number in self.cpu_model_info.cpu_dict["counts_by_model"]:
                result += f"# Selected copy counts from '{epyc_model_number}' section of CPU info" + self.EOL
                result += self.add_counts_section(self.cpu_model_info.cpu_dict["counts_by_model"][epyc_model_number])

            # Then try by type x cores per NUMA node
            elif cpu_type_and_size in self.cpu_model_info.cpu_dict["counts_by_type"]:
                result += f"# Selected copy counts from '{cpu_type_and_size}' section of CPU info" + self.EOL
                result += self.add_counts_section(self.cpu_model_info.cpu_dict["counts_by_type"][cpu_type_and_size])

            # Then try by core counts alone
            elif physical_cores_tag in self.cpu_model_info.cpu_dict["counts_by_core_count"]:
                result += f"# Selected copy counts from '{physical_cores_tag}' section of CPU info" + self.EOL
                result += self.add_counts_section(self.cpu_model_info.cpu_dict["counts_by_core_count"][physical_cores_tag])
            elif logical_cores_tag in self.cpu_model_info.cpu_dict["counts_by_core_count"]:
                result += f"# Selected copy counts from '{logical_cores_tag}' section of CPU info" + self.EOL
                result += self.add_counts_section(self.cpu_model_info.cpu_dict["counts_by_core_count"][logical_cores_tag])

            # Finally, use the default if there is one
            elif "counts_default" in self.cpu_model_info.cpu_dict:
                result += f"# Selected copy counts from default section of CPU info (nothing for {epyc_model_number}, {cpu_type_and_size}, {physical_cores_tag}, or {logical_cores_tag})" + self.EOL
                result += self.add_counts_section(self.cpu_model_info.cpu_dict["counts_default"])

        else:
            if self.cores_affinity_list != []:
                result += self.get_default_base_peak_copies_block('default', self.cores_affinity_list)
            elif self.rate_copies == self.number_of_logical_cores_total:
                result += self.get_default_base_peak_copies_block('default', range(0, self.number_of_logical_cores_total))
            elif self.rate_copies == self.number_of_physical_cores_total:
                result += self.get_default_base_peak_copies_block('default', range(0, self.number_of_physical_cores_total))
            else:
                print( 'self.number_of_physical_cores_total = ' + str(self.number_of_physical_cores_total ) )
                stride = round( self.number_of_physical_cores_total / self.rate_copies )
                print( 'stride = ' + str(stride) )
                if self.affinity_type.lower() == 'dell':
                    affinity_list = range(0, self.rate_copies)
                else:
                    affinity_list = range(0, self.number_of_physical_cores_total, stride)
                result += self.get_default_base_peak_copies_block('default', affinity_list)
                print( result )

        result += '# Switch back to the default block after the include file:' + self.EOLx2
        result += 'default:' + self.EOL
        result += self.HASH_LINEx2
        return result

    def add_counts_section(self, counts):
        section = ""

        for section_name in [x for x in counts if x in ("default", "specrate", "intrate", "fprate") or x.startswith("5")]:
            try:
                copy_count_type = counts[section_name]["copy_count"]
                copy_count = self.quantities_map[copy_count_type]
                if section_name == "default" or section_name.endswith("rate"):
                    section += self.get_default_base_peak_copies_block(section_name, copy_count)
                elif section_name.startswith("5"):
                    benchmark_numbers = list(map(int, section_name.split(",")))
                    section += self.get_default_base_peak_copies_block(self.get_benchmark_string(benchmark_numbers), copy_count)
            except KeyError:
                if copy_count_type:
                    print(f"ERROR: No conversion from '{copy_count_type}' to core list")
                else:
                    print(f"ERROR: No copy counts for '{section_name}' in {copy_count_type} section of CPU info")
            except TypeError:
                print(f"ERROR: Benchmark specifications in CPU info must be by benchmark number only")

        return section
