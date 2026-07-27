SAH=/lustre/fsw/portfolios/av/users/yingzim/code/self_adapt_harness
IN=$SAH/ahc_work/cache/public_inputs_150/ahc039_inputs/ahc039_000000_input.txt
ls -la /usr/bin/time 2>&1 | head -1
echo "--- composite WITH sync:"
time timeout 8 bash -c "prlimit --cpu=3.1 /usr/bin/time -f '%e' -o /tmp/prof.txt /tmp/m2_bin 2.0 < $IN > /tmp/o3.txt; sync"; echo "rc=$?"
echo "--- composite WITHOUT sync:"
time timeout 8 bash -c "prlimit --cpu=3.1 /usr/bin/time -f '%e' -o /tmp/prof2.txt /tmp/m2_bin 2.0 < $IN > /tmp/o4.txt"; echo "rc=$?"
