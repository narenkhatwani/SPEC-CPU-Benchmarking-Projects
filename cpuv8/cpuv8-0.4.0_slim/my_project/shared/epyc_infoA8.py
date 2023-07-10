#!/bin/env python3

# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 12:34:24 2020

@author: vsmith
"""

import json
import os
from . import sys_info as sys_info

########################################################################
#                                                                      #
# Licensed per Software License Clickwrap (SPPO).PDF document          #
#                                                                      #
# PURPOSE: Provides a library of commonly used EPYC information        #
#          routines.                                                   #
#                                                                      #
# VERSION: 1.0.11                                                       #
#                                                                      #
########################################################################

class CpuModels:
    
    JSON_FILENAME = 'cpu_info.json'
    cpu_str = ''
    cpu_dict = None
    __version__ = "1.0.11"

    def __init__(self, a_json_filename=None):
        if a_json_filename is None:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            a_json_filename = dir_path + '/' + self.JSON_FILENAME
        else:
            self.JSON_FILENAME = a_json_filename
        self.cpu_dict = self.fill_dict_from_json_file(a_json_filename)

    #staticmethod        
    def fill_dict_from_json_file(self, a_json_filename):
        json_file = open(a_json_filename)
        self.cpu_str = json_file.read()
        json_file.close()
        result = json.loads(self.cpu_str)
        return result
        
    def find_cpu_model(self, a_cpu_model):
        a_cpu_model = a_cpu_model.lower()
        try:
            return next(cpu for cpu in self.cpu_dict['cpu_models'] \
                if cpu['cpu_model'] == a_cpu_model)
        except StopIteration:
            print(f"WARNING: '{a_cpu_model}' isn't in the CPU info DB; informational fields in the result will be incorrect.")
            print(f"If possible, enter '{a_cpu_model}' information into '{self.JSON_FILENAME}'.")
            return self.cpu_dict.get('unknown_cpu', {
                    "cpu_model": "unknown",
                    "codename": "unknown",
                    "release_date": "unknown",
                    "physical_core_count": 1,
                    "logical_core_count": 1,
                    "clock_speed_nominal": 1,
                    "clock_speed_boost_all_cores": 1,
                    "clock_speed_boost_max": 1,
                    "smt_enabled": True,
                    "smt_capable": True,
                    "tdp": 1,
                    "ctp_min": 1,
                    "ctp_max": 1,
                    "l1d_kb": 1,
                    "l1i_kb": 1,
                    "l2_kb": 1,
                    "l3_mb": 1,
                    "l3_mb_per_core": "0",
                    "memory_mts_max": 1,
                    "memory_channels": 1,
                    "socket_count_max": 1,
                    "pcie": "unknown",
                    "tj": 1,
                    "package": "unknown",
                    "ccd_count": 1,
                    "ccx_count": 1,
                    "numa_node_count": 1
                    })


class CpuInfo:
    
    __cpu_model = None
    @property
    def cpu_model(self):
        return self.__cpu_model

    def __init__(self, a_model_number='9654', a_smt_enabled=True, a_ctdp=0, \
                 a_max_ddr4_mhz=0):
        self.smt_enabled = a_smt_enabled
        self.model_number = a_model_number
        self.ctdp = a_ctdp
        self.max_ddr4_mhz = a_max_ddr4_mhz
        self.__cpu_model = self.get_cpu_model(a_model_number)

    def get_cpu_model(self, a_model_number):
        cpu_info = CpuModels()
        result = cpu_info.find_cpu_model(a_model_number)
        if result['cpu_model'] == "unknown":
            cpu_arch = ""
            if sys_info.is_cpu_bergamo():
                cpu_arch = 'Bergamo'
            elif sys_info.is_cpu_genoa():
                cpu_arch = 'Genoa'
            elif sys_info.is_cpu_rome():
                cpu_arch = "Rome"
            elif sys_info.is_cpu_milan():
                cpu_arch = "Milan"
            elif sys_info.is_cpu_milanx():
                cpu_arch = "Milanx"
            elif sys_info.is_cpu_naples():
                cpu_arch = "Naples"
            if cpu_arch != "":
                print(f"Using generic model '{a_model_number}'.")
                a_model_number = cpu_arch + str(sys_info.get_physical_cores_per_socket())
                result = cpu_info.find_cpu_model(a_model_number)
        return result

    @property
    def model_number(self):
        return self.__cpu_model['cpu_model']
    @model_number.setter
    def model_number(self, value):
        self.__cpu_model = self.get_cpu_model(value)
    
    __smt_enabled = True
    @property
    def smt_enabled(self):
        return self.__smt_enabled
    @smt_enabled.setter
    def smt_enabled(self,value):
        self.__smt_enabled = value

    @property
    def logical_core_count(self):        
        if self.__smt_enabled:
            return 2 * self.physical_core_count
        else:
            return self.physical_core_count    

    @property
    def physical_core_count(self):
        return int(self.__cpu_model['physical_core_count'])

    __cpu_is_known = True
    @property
    def cpu_is_known(self):
        return self.__cpu_is_known
    @cpu_is_known.setter
    def cpu_is_known(self, value):
        self.__cpu_is_known = value

    @property
    def clock_speed_nominal(self):
        return int(self.__cpu_model['clock_speed_nominal'])

    @property
    def clock_speed_boost_max(self):
        return int(self.__cpu_model['clock_speed_boost_max'])

    @property
    def clock_speed_boost_all_cores(self):
        return int(self.__cpu_model['clock_speed_boost_all_cores'])

    @property
    def tdp(self):
        return int(self.__cpu_model['tdp'])

    __ctdp = 0
    @property
    def ctdp(self):
        return self.__ctdp
    @ctdp.setter
    def ctdp(self, value):
        if (value != 0) and ((value < self.ctdp_min) or (value > self.ctdp_max)):
            print('WARNING: you are setting ctdp outside of allowed values.')
            print('ctdp (W): ' + str(value))
            print('tdp min (W): ' + str(self.ctdp_min))
            print('tdp max (W): ' + str(self.ctdp_max))
        self.__ctdp = value

    @property
    def ctdp_min(self):
        return int(self.__cpu_model['ctp_min'])

    @property
    def ctdp_max(self):
        return int(self.__cpu_model['ctp_max'])
        
    @property
    def l1d_kib(self):
        return int(self.__cpu_model['l1d_kb'])

    @property
    def l1i_kib(self):
        return int(self.__cpu_model['l1i_kb'])

    @property
    def l2_kib(self):
        return int(self.__cpu_model['l2_kb'])

    @property
    def l3_mib(self):
        return int(self.__cpu_model['l3_mb'])
    
    @property
    def l3_mb_per_core(self):
        return self.__cpu_model['l3_mb_per_core']

    @property
    def ddr4_mHz_max(self):
        return int(self.__cpu_model['memory_mts_max'])

    @property
    def ddr4_channels(self):
        return int(self.__cpu_model['memory_channels'])

    @property
    def socket_count_max(self):
        return int(self.__cpu_model['socket_count_max'])

    @property
    def pcie(self):
        return int(self.__cpu_model['pcie'])

    @property
    def tj(self):
        return int(self.__cpu_model['tj'])

    @property
    def package(self):
        return int(self.__cpu_model['package'])

    @property
    def codename(self):
        return int(self.__cpu_model['codename'])

'''
my_epyc_info = CpuModels()
cpu_str = my_epyc_info.cpu_str
print(cpu_str)
cpu_dict = my_epyc_info.cpu_dict
#print(cpu_dict['cpu_models'])
cpu_model = my_epyc_info.find_cpu_model('7742')
print(cpu_model)
'''
