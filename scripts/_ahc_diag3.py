import json, os, pathlib, subprocess, sys
DS = "/lustre/fsw/portfolios/av/users/yingzim/datasets/self_adapt_harness/raw/simpletes-b7e0367/datasets/ahc"
SAH = "/lustre/fsw/portfolios/av/users/yingzim/code/self_adapt_harness"
ns = {}
exec(pathlib.Path(f"{DS}/ahc039/init_program.py").read_text(), ns)  # proper extraction
pathlib.Path("/tmp/M2.cpp").write_text(ns["CPP_CODE"])
print("cpp len:", len(ns["CPP_CODE"]))
r = subprocess.run([sys.executable, f"{DS}/docker_runner.py", "/tmp/M2.cpp",
    f"{SAH}/ahc_work/cache/public_inputs_150/ahc039_inputs",
    f"{SAH}/ahc_work/cache/tester_binaries/ahc039_tester", "5", "5", "2.0"],
    capture_output=True, text=True, timeout=400, env=dict(os.environ))
d = json.loads(r.stdout.splitlines()[-1])
for c in d["case_results"]:
    print(c["case_idx"], c["judge"], c["score"], c["msg"][:50], round(c["time"], 2))
