################################################################################
# AMD GCC 13.0 SPEC CPU2017 V1.1.9 Rate Configuration Flags for AMD64 Linux
################################################################################
# Compilers
################################################################################

default:

CC                       = gcc -m64 -std=c18
CXX                      = g++ -m64 -std=c++17
FC                       = gfortran -m64 -std=f2008
CLD                      = gcc -m64
CXXLD                    = g++ -m64
FLD                      = gfortran -m64
CC_VERSION_OPTION        = -v
CXX_VERSION_OPTION       = -v
FC_VERSION_OPTION        = -v

################################################################################
# Default libraries and variables
################################################################################

default:

# Libraries:

# Don't put the AMD and mvec math libraries in MATH_LIBS because it will trigger a reporting issue
# because GCC won't use them. Forcefeed all benchmarks the math libraries in EXTRA_LIBS and clear
# out MATH_LIBS.
MATH_LIBS               =
MATHLIBOPT               = #clear this variable or else SPEC will set it to -lm
VECMATHLIB               = -fveclib=AMDLIBM
EXTRA_LIBS               = -lamdalloc -lamdlibm -lm
EXTRA_FLIBS              = -lmvec -lamdlibm -lm

# Portability flags include file:
include: %{port_flags_inc_file_name}

# Workaround flags include file:
include: %{workaround_flags_inc_file_name}

################################################################################
# Tuning Flags
################################################################################

#####################
# Base tuning flags #
#####################

default=base:

COPTIMIZE                = -O2 \
                           -march=znver3 \
                           -flto

CXXOPTIMIZE              = -O2 \
                           -march=znver3 \
                           -flto

FOPTIMIZE                = -O2 \
                           -march=znver3 \
                           -flto


########################
# specrate tuning flags #
########################

specrate:

# Libraries:
EXTRA_LIBS               = -lamdlibm -lm
EXTRA_CLIBS              = -lamdalloc
EXTRA_CXXLIBS            = -lamdalloc-ext
EXTRA_FLIBS              = -lamdalloc


#####################
# Peak tuning flags #
#####################

default=peak:

COPTIMIZE                = -Ofast \
                           -march=znver3 \
                           -flto

CXXOPTIMIZE              = -Ofast \
                           -march=znver3 \
                           -flto

FOPTIMIZE                = -Ofast \
                           -march=znver3 \
                           -flto

# Feedback is only allowed in peak.
# Disable it for now:
feedback                 = 0
PASS1_CFLAGS             = -fprofile-instr-generate
PASS2_CFLAGS             = -fprofile-instr-use
PASS1_FFLAGS             = -fprofile-generate
PASS2_FFLAGS             = -fprofile-use
PASS1_CXXFLAGS           = -fprofile-generate
PASS2_CXXFLAGS           = -fprofile-instr-use
PASS1_LDFLAGS            = -fprofile-instr-generate
PASS2_LDFLAGS            = -fprofile-instr-use
fdo_run1                 = $command ; llvm-profdata merge --output=default.profdata *.profraw


# Benchmark specific peak tuning flags:

# 721.gcc_r=peak:
CC                       = gcc -m32
