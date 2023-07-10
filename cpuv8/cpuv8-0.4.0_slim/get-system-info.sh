config_file=$1
#gather some data about this run and dump it with the results
mkdir -p result
hostname > result/configinfo.txt 2>&1
date >> result/configinfo.txt 2>&1
echo >> result/configinfo.txt 2>&1
echo PATH=$PATH >> result/configinfo.txt 2>&1
echo >> result/configinfo.txt 2>&1
echo LD_LIBRARY_PATH=$LD_LIBRARY_PATH >> result/configinfo.txt 2>&1
echo >> result/configinfo.txt 2>&1
echo LIBRARY_PATH=$LIBRARY_PATH >> result/configinfo.txt 2>&1
echo >> result/configinfo.txt 2>&1
echo >> result/configinfo.txt 2>&1
echo "***** clang -v *****" >> result/configinfo.txt 2>&1
echo >> result/configinfo.txt 2>&1
clang -v >> result/configinfo.txt 2>&1
echo >> result/configinfo.txt 2>&1
echo "***** clang++ -v *****" >> result/configinfo.txt 2>&1
echo >> result/configinfo.txt 2>&1
clang++ -v >> result/configinfo.txt 2>&1
echo >> result/configinfo.txt 2>&1
echo "***** gfortran -v *****" >> result/configinfo.txt 2>&1
echo >> result/configinfo.txt 2>&1
gfortran -v >> result/configinfo.txt 2>&1
echo >> result/configinfo.txt 2>&1
cat /proc/meminfo >> result/configinfo.txt 2>&1
cat /sys/devices/system/node/node*/meminfo >> result/configinfo.txt 2>&1
echo >> result/configinfo.txt 2>&1
cat /proc/cpuinfo | grep -m 1 "model name" >> result/configinfo.txt 2>&1
cat /proc/cpuinfo | grep -m 1 "cpu MHz" >> result/configinfo.txt 2>&1
echo >> result/configinfo.txt 2>&1
dmidecode -t bios >> result/configinfo.txt 2>&1
echo >> result/configinfo.txt 2>&1
cat /etc/*elease >> result/configinfo.txt 2>&1
uname -a >> result/configinfo.txt 2>&1
df -H >> result/configinfo.txt 2>&1 
echo >> result/configinfo.txt 2>&1
echo >> result/configinfo.txt 2>&1
echo "***** which gfortran *****" >> result/configinfo.txt 2>&1
echo >> result/configinfo.txt 2>&1
which gfortran >> configinfo >> result/configinfo.txt 2>&1
echo >> result/configinfo.txt 2>&1
echo "***** which gcc *****" >> result/configinfo.txt 2>&1
echo >> result/configinfo.txt 2>&1
which gcc >> result/configinfo.txt 2>&1

cp config/$config_file result/