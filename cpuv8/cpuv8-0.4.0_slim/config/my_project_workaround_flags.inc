################################################################################
# AMD GCC 13.0.0 SPEC CPU2017 V1.1.9 Rate Workaround Flags for AMD64 Linux
################################################################################
#----------------------------------------------------------------------
#       GCC workarounds that do not count as PORTABILITY
#----------------------------------------------------------------------
# The workarounds in this section would not qualify under the SPEC CPU
# PORTABILITY rule.
#   - In peak, they can be set as needed for individual benchmarks.
#   - In base, individual settings are not allowed; set for whole suite.
# See:
#     https://www.spec.org/cpu2017/Docs/runrules.html#portability
#     https://www.spec.org/cpu2017/Docs/runrules.html#BaseFlags

#######################
# Default workarounds #
#######################
#
# *** NONE ***
#

####################
# Base workarounds #
####################
#
# *** NONE ***
#


##############################
# specrate workarounds - peak #
##############################

# 721.gcc_r=peak: # https://www.spec.org/cpu2017/Docs/benchmarks/502.gcc_r.html
EXTRA_CFLAGS             = -fno-strict-aliasing \
                           -fgnu89-inline


# 709.cactus_r=peak: #lang='CXX'
EXTRA_CXXFLAGS           = -fpermissive

# 710.omnetpp_r=peak:      #lang='CXX'
# Fixes RE:
CXXOPTIMIZE              = -std=c++03


##############################
# specrate workarounds - base #
##############################
# Combine the int peak above - https://www.spec.org/cpu2017/Docs/runrules.html#BaseFlags
# Combine the FP peak above - https://www.spec.org/cpu2017/Docs/runrules.html#BaseFlags

specrate=base:
EXTRA_CFLAGS             = -fno-strict-aliasing \
                           -fno-unsafe-math-optimizations \
                           -fno-finite-math-only \
                           -fgnu89-inline \
                           -fcommon \
                           -std=c99

EXTRA_CXXFLAGS           = -std=c++03 \
                           -fpermissive

EXTRA_FFLAGS             = -std=legacy \
                          -fallow-argument-mismatch
