################################################################################
#   AMD GCC 13.0.0 SPEC CPU2017 V1.1.9 Rate Portability Flags for AMD64 Linux  #
################################################################################
default:
# data model applies to all benchmarks
EXTRA_PORTABILITY        = -DSPEC_LP64

# *** Benchmark-specific portability ***
# Anything other than the data model is only allowed where a need is proven.
# (ordered by last 2 digits of benchmark number)

# 706.stockfish_r:
PORTABILITY              = -pthread
EXTRA_PORTABILITY = -DSPEC_LP64

# 743.lua_r:
PORTABILITY = -DLUA_USE_LINUX

# 745.brotli_r:
PORTABILITY = -DOS_LINUX

# 779.mdgb_r:
PORTABILITY = -fopenmp
################################################################################
# End Portabilty Flags
################################################################################
