SAH=/lustre/fsw/portfolios/av/users/yingzim/code/self_adapt_harness
IN=$SAH/ahc_work/cache/public_inputs_150/ahc039_inputs/ahc039_000000_input.txt
g++ -std=gnu++20 -O2 -o /tmp/m2_bin /tmp/M2.cpp 2>/dev/null || python3 -c "
import pathlib
ns = {}
exec(pathlib.Path('/lustre/fsw/portfolios/av/users/yingzim/datasets/self_adapt_harness/raw/simpletes-b7e0367/datasets/ahc/ahc039/init_program.py').read_text(), ns)
pathlib.Path('/tmp/M2.cpp').write_text(ns['CPP_CODE'])" && g++ -std=gnu++20 -O2 -o /tmp/m2_bin /tmp/M2.cpp
echo "--- run WITHOUT argv:"; time timeout 8 /tmp/m2_bin < "$IN" > /tmp/o1.txt; echo "rc=$?"
echo "--- run WITH argv 2.0:"; time timeout 8 /tmp/m2_bin 2.0 < "$IN" > /tmp/o2.txt; echo "rc=$?"
echo "--- prlimit float test:"; prlimit --cpu=3.1 true; echo "rc=$?"
echo "--- prlimit int test:"; prlimit --cpu=3 true; echo "rc=$?"
$SAH/ahc_work/cache/tester_binaries/ahc039_tester "$IN" /tmp/o2.txt 2>&1 | tail -1
