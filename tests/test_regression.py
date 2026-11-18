import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from src.regression import wilson_interval, mcnemar, ci_gate

def test_wilson_bounds():
    lo, hi = wilson_interval(80, 100)
    assert 0.0 <= lo < 0.8 < hi <= 1.0
def test_wilson_empty():
    assert wilson_interval(0, 0) == (0.0, 0.0)
def test_mcnemar_no_discordant():
    assert mcnemar(0, 0) == (0.0, 1.0)
def test_ci_gate_blocks_big_drop():
    assert ci_gate(0.90, 0.80)["blocked"] is True
    assert ci_gate(0.90, 0.88)["blocked"] is False
