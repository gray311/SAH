export AHC_NATIVE=1 AHC_CXX=g++ AHC_NUM_CASES=6 AHC_CASE_WORKERS=6
SAH=/lustre/fsw/portfolios/av/users/yingzim/code/self_adapt_harness
export AHC_CACHE_DIR=$SAH/ahc_work/cache
DS=/lustre/fsw/portfolios/av/users/yingzim/datasets/self_adapt_harness/raw/simpletes-b7e0367/datasets/ahc
python3 - <<'PY'
import re, pathlib, subprocess, json, sys, os
DS = "/lustre/fsw/portfolios/av/users/yingzim/datasets/self_adapt_harness/raw/simpletes-b7e0367/datasets/ahc"
SAH = "/lustre/fsw/portfolios/av/users/yingzim/code/self_adapt_harness"
src = pathlib.Path(f"{DS}/ahc039/init_program.py").read_text()
m = re.search(r"CPP_CODE = '''(.*?)'''", src, re.S)
pathlib.Path("/tmp/M.cpp").write_text(m.group(1))
r = subprocess.run([sys.executable, f"{DS}/docker_runner.py", "/tmp/M.cpp",
  f"{SAH}/ahc_work/cache/public_inputs_150/ahc039_inputs",
  f"{SAH}/ahc_work/cache/tester_binaries/ahc039_tester", "6", "6", "2.0"],
  capture_output=True, text=True, timeout=400, env=dict(os.environ))
print("stderr:", r.stderr[-200:] if r.stderr else "")
d = json.loads(r.stdout.splitlines()[-1])
for c in d["case_results"]:
    print(c["case_idx"], c["judge"], c["score"], c["msg"][:40], round(c["time"],2))
PY
