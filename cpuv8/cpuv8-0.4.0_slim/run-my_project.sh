#!/usr/bin/bash

# Enter your project name below.
# Your config files and library folder need this name.
PROJECT_NAME="my_project"

# Enter the benchmarks that you want to run:
BENCHMARKS="788"

# Enter the number of copies you want to run.
# $(nproc) = # of available hardware threads.
# Note that the copies will run without affinity unless you configure
# affinity in the include file.
#COPIES=$(nproc)
COPIES=1

# Enter the workloads that you want to run.
# Options are test, train, ref, all (space delimited):
WORKLOADS="all"

# Tuning: options are base, peak, all (space delimited):
TUNE="all"

# Set the number of times you want to run the benchmarks:
ITERATIONS=1

# Do you want a reportable run, which is required for submissions?
# Note that neither builds not runs will succeed if you specify reportable
# but have converted your SPEC CPU installation kit to development.
# Also be aware that reportable runs have a minumum of two iterations.
REPORTABLE=false

# You should not have to modify anything beyond this line.
CWD=$(pwd)
export LD_LIBRARY_PATH=${CWD}/${PROJECT_NAME}
# Set the SPEC CPU file paths to enable SPEC commands:
. ./shrc
if [ $REPORTABLE = true ] ; then
  # We recommend a minimum of three iterations for a reportable run:
  runcpu --config ${PROJECT_NAME}.cfg --iterations 3 --reportable --tune $TUNE --copies $COPIES $BENCHMARKS
else
  runcpu --config ${PROJECT_NAME}.cfg --iterations $ITERATIONS --noreportable --size $WORKLOADS --tune $TUNE --ignoreerror --copies $COPIES $BENCHMARKS
fi
