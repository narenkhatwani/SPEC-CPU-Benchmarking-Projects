runcpu --config=comments --fakereport | grep txt
echo 
echo From the report:
grep "This note"   /tmp/comments/result/CPUv8.001*txt
echo 
echo From --output_format=config
grep '#'           /tmp/comments/result/CPUv8.001.fprate.test.orig.cfg
# see "Stupid Assumptions" in tiny-examples/contents.txt
