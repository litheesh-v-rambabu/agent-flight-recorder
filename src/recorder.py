"""Structured span recording for LLM agent runs, backed by SQLite (stdlib only)."""
import sqlite3, json, time
from dataclasses import dataclass, asdict

@dataclass
class Span:
    run_id: str
    task_id: str
    step_type: str  # llm | tool | retrieval
    name: str
    status: str = "ok"  # ok | error | timeout
    latency_ms: float = 0.0
    error: str = ""
    ts: float = 0.0

class Recorder:
    def __init__(self, db_path=":memory:"):
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("""CREATE TABLE IF NOT EXISTS spans(
            run_id TEXT, task_id TEXT, step_type TEXT, name TEXT,
            status TEXT, latency_ms REAL, error TEXT, ts REAL)""")
    def record(self, span: Span):
        if not span.ts: span.ts = time.time()
        d = asdict(span)
        self.conn.execute("INSERT INTO spans VALUES (:run_id,:task_id,:step_type,:name,:status,:latency_ms,:error,:ts)", d)
        self.conn.commit()
    def spans_for_run(self, run_id):
        cur = self.conn.execute("SELECT run_id,task_id,step_type,name,status,latency_ms,error,ts FROM spans WHERE run_id=?", (run_id,))
        return [Span(*r) for r in cur.fetchall()]
    def run_ids(self):
        return [r[0] for r in self.conn.execute("SELECT DISTINCT run_id FROM spans")]
    def failed_runs(self):
        return [r[0] for r in self.conn.execute("SELECT DISTINCT run_id FROM spans WHERE status!='ok'")]
