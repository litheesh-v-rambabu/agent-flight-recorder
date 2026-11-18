import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from src.recorder import Recorder, Span
from src.scoring import detect_failure

def test_record_and_failed_runs():
    r = Recorder()
    r.record(Span("run-1","task-1","llm","llm_call","ok",120))
    r.record(Span("run-2","task-1","tool","search","error",0,"boom"))
    assert set(r.run_ids()) == {"run-1","run-2"}
    assert r.failed_runs() == ["run-2"]
def test_detect_failure():
    bad,_ = detect_failure([Span("r","t","tool","x","error",0,"e")])
    good,_ = detect_failure([Span("r","t","llm","x","ok",100)])
    assert bad is True and good is False
