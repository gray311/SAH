set -x
SAH=/lustre/fsw/portfolios/av/users/yingzim/code/self_adapt_harness
DS=/lustre/fsw/portfolios/av/users/yingzim/datasets/self_adapt_harness/raw/simpletes-b7e0367/datasets/ahc
python3 -c "
import re, pathlib
src = pathlib.Path('$DS/ahc039/init_program.py').read_text()
m = re.search(r\"CPP_CODE = '''(.*?)'''\", src, re.S)
pathlib.Path('/tmp/M.cpp').write_text(m.group(1))"
g++ -std=gnu++20 -O2 -o /tmp/m_bin /tmp/M.cpp 2>/dev/null; echo "compile rc=$?"
IN=$SAH/ahc_work/cache/public_inputs_150/ahc039_inputs/ahc039_000000_input.txt
time timeout 9 /tmp/m_bin < "$IN" > /tmp/m_out.txt; echo "run rc=$?"
wc -l /tmp/m_out.txt; head -2 /tmp/m_out.txt
$SAH/ahc_work/cache/tester_binaries/ahc039_tester "$IN" /tmp/m_out.txt
