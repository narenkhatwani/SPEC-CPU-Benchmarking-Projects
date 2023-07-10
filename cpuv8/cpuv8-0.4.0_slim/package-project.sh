#!/usr/bin/env bash

# Enter project name (config file and library folder name):
PROJECT_NAME="my_project"

# It should not be necessary to modify anything beyond this point.
rm -rf lib/__pycache__
tar -cJvf ${PROJECT_NAME}.tar.xz setenv_build_libs_rate.sh get-system-info.sh gcc13-flags.xml build-${PROJECT_NAME}.sh run-${PROJECT_NAME}.sh ${PROJECT_NAME} config package-project.sh
