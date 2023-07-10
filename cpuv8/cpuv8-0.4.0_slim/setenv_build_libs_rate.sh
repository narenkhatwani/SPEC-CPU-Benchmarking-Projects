PROJECT_NAME="my_project"
# Needed for AOCC builds (update for new AOCC versions):
#source /opt/AMD/aocc/setenv_AOCC.sh
# Add AOCL:
#source /opt/AMD/aocl/2208/amd-libs.cfg
#AOCL_PATH=$AOCL_ROOT/lib

CWD=$(pwd)
BASE_DIR=${CWD}/${PROJECT_NAME}

# set library paths:
LIB_PATH=$BASE_DIR/lib
LIB32_PATH=$BASE_DIR/lib32
export LIBRARY_PATH=$AOCL_PATH:$LIB_PATH:$LIB32_PATH:$LIBRARY_PATH
export LD_LIBRARY_PATH=$AOCL_PATH:$LIB_PATH:$LIB32_PATH:$LD_LIBRARY_PATH
