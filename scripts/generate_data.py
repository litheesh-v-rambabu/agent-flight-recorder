"""Generate deterministic synthetic demo traces: ~700 runs across 120 tasks (seed 42).
Demo/sample data only — not production traces."""
import csv, random, pathlib
FAIL_MODES = ["timeout:search_tool","error:calculator","empty_tool_result","slow_step:llm","schema_error"]
def main():
    rng = random.Random(42)
    out = pathlib.Path(__file__).resolve().parents[1]/"data"; out.mkdir(exist_ok=True)
    path = out/"demo_traces.csv"
    with open(path,"w",newline="") as f:
        wr = csv.writer(f); wr.writerow(["run_id","task_id","step_type","name","status","latency_ms","error"])
        for i in range(700):
            task = f"task-{rng.randint(1,120):03d}"
            failed = rng.random() < 0.22
            status = "error" if failed else "ok"
            wr.writerow([f"run-{i:04d}", task, rng.choice(["llm","tool","retrieval"]),
                         rng.choice(["llm_call","search_tool","calculator","retrieve"]),
                         status, round(rng.uniform(50,4500),1), rng.choice(FAIL_MODES) if failed else ""])
    print(f"Wrote {path} (700 demo runs, 120 tasks, seed 42)")
if __name__ == "__main__": main()
