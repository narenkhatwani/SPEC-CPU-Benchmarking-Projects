#!/bin/bash

# config_file: This is the name of the SPEC CPU2017 configuration file.
# This is usually the only thing that you need to change with new binaries.
config_file="my_project.cfg"

# Abort the build if the allow_build flag is set to false in the config file:
if grep -i "%define\s*allow_build\s*false" config/$config_file; then
  echo; echo "You have the 'allow_build' flag set to 'false' in config/"$config_file". You must set this flag to 'true' to build CPU2017."
  echo; echo "Exiting script."
  echo
  exit 1
fi

# Clear the screen and show config_file:
clear
echo "config_file = $config_file"
echo
echo "Sleeping for five seconds..."
sleep 5
echo "Continuing..."
echo

# set library paths (edit setenv_build_libs_rate.sh for new binaries):
. ./setenv_build_libs_rate.sh

# You should not need to edit anything further unless you intend custom builds.

# The following ulimit commands require the root user:
ulimit -s unlimited
ulimit -l 2097152

# Source the CPU2017 environment:
. ./shrc

echo "LD_LIBRARY_PATH = $LD_LIBRARY_PATH"
echo
echo "LIBRARY_PATH = $LIBRARY_PATH"
echo
echo "AOCL_ROOT = $AOCL_ROOT"
echo
echo "PATH = $PATH"
echo


# Call the script to dump diagnostic system information into the result directory:
./get-system-info.sh $config_file

# CPUv8 benchmarks:
# ==================
# 800.pot3d_s	701.xz_r	801.xz_s	803.sph_exa_s	804.hpgmgfv_s	705.lbm_r	805.lbm_s	706.stockfish_r	806.stockfish_s	707.ntest_r	807.ntest_s	708.sqlite_r	709.cactus_r	809.cactus_s	710.omnetpp_r	810.omnetpp_s	711.tealeaf_r	811.tealeaf_s	712.av1aom_r	714.cpython_r	715.lammps_r	716.nab_r	816.nab_s	717.flac_r	718.bude_r	818.bude_s	820.cloverleaf_s	721.gcc_r	821.gcc_s	722.palm_r	822.palm_s	723.llvm_r	725.opus_r	726.saga_r	826.saga_s	727.cppcheck_r	827.cppcheck_s	728.tesseract_r	828.tesseract_s	729.abc_r	829.abc_s	731.astcenc_r	733.mlpack_r	734.vpr_r	834.vpr_s	735.gem5_r	737.gmsh_r	837.gmsh_s	738.diamond_r	838.diamond_s	739.xsbench_r	839.xsbench_s	740.rsbench_r	840.rsbench_s	742.simpoint_r	842.simpoint_s	743.lua_r	744.dcraw_r	745.brotli_r	746.minizinc_r	747.sampleflow_r	847.sampleflow_s	748.flightdm_r	749.fotonik3d_r	849.fotonik3d_s	750.homoencrypt_r	752.whisper_r	852.whisper_s	777.zstd_r	998.specrand_s	999.specrand_r

# benchmarks: options are "specrate", "fprate", "intrate" or any combination of
# the rate benchmarks above (e.g. "701 710 707")
benchmarks="788"

# tuning: options are "base", "peak", "all":
tuning="all"

# Uncomment the line below and comment out the rest of the file if you intend custom builds:
runcpu --action=build --rebuild --config $config_file --ignore_errors --tune $tuning $benchmarks

