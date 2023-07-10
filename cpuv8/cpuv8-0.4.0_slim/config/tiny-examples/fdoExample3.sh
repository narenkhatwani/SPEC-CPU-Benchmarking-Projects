runcpu --config=fdoExample3 --fake | grep "log for"
grep -n '%% Fake commands' /tmp/fake/result/CPUv8.001.log \
    | cut -f 1-5 -d' ' 
# see "Stupid Assumptions" in tiny-examples/contents.txt
