"""Failure detection: rule-based checks + a local LLM-as-judge-STYLE heuristic.

No paid API key is used in this demo. `judge_score` is a transparent heuristic
that mimics the interface of an LLM judge so the pipeline can run offline.
"""
def rule_checks(spans):
    issues = []
    for s in spans:
        if s.status == "timeout": issues.append("timeout")
        if s.status == "error": issues.append(f"error:{s.name}")
        if s.step_type == "tool" and s.latency_ms == 0: issues.append("empty_tool_result")
        if s.latency_ms > 5000: issues.append("slow_step")
    return issues

def judge_score(spans):
    """Return 0..1 quality score (1 = healthy). Local heuristic, NOT an LLM."""
    if not spans: return 0.0
    score = 1.0
    for s in spans:
        if s.status == "error": score -= 0.35
        if s.status == "timeout": score -= 0.3
        if s.error: score -= 0.1
    return max(0.0, min(1.0, score))

def detect_failure(spans, threshold=0.7):
    issues = rule_checks(spans)
    return (judge_score(spans) < threshold or bool(issues)), issues
