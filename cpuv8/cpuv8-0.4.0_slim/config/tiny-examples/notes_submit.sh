runcpu --config=notes_submit 999.specrand_r --tune=base | grep txt
runcpu --config=notes_submit 998.specrand_s --tune=base | grep txt
runcpu --config=notes_submit 998.specrand_s --tune=peak | grep txt

echo
grep -C1 "to prefer" /tmp/notes_submit/result/CPUv8.00*txt

cd /tmp/notes_submit/benchspec/CPU/999.specrand_r/run/
  num_dirs=$(ls -d run* | wc -l)
 num_dobmk=$(ls run*/dobmk | wc -l)
echo
echo 999.specrand_r has $num_dirs run dirs and $num_dobmk dobmk scripts

cd /tmp/notes_submit/benchspec/CPU/998.specrand_s/run/
      num_dirs_base=$(ls -d run*base* | wc -l)
      num_dirs_peak=$(ls -d run*peak* | wc -l)
 num_dobmk_base=$(ls run*base*/dobmk | wc -l)
 num_dobmk_peak=$(ls run*peak*/dobmk 2>/dev/null | wc -l)
echo
echo "998.specrand_s base has $num_dirs_base run dir(s) and $num_dobmk_base dobmk script(s)"
echo "998.specrand_s peak has $num_dirs_peak run dir(s) and $num_dobmk_peak dobmk script(s)"
# see "Stupid Assumptions" in tiny-examples/contents.txt
