"""Version comparison statistics: Wilson intervals + McNemar + CI gate.
Pure python + scipy (scipy used only for the chi-square survival function,
with a math fallback)."""
import math
try:
    from scipy.stats import chi2
    def _chi2_sf(x, df=1): return float(chi2.sf(x, df))
except Exception:
    def _chi2_sf(x, df=1): return math.erfc(math.sqrt(x/2))  # df=1 approx

def wilson_interval(successes, n, z=1.96):
    if n == 0: return (0.0, 0.0)
    p = successes / n
    denom = 1 + z*z/n
    centre = (p + z*z/(2*n)) / denom
    half = (z * math.sqrt(p*(1-p)/n + z*z/(4*n*n))) / denom
    return (max(0.0, centre-half), min(1.0, centre+half))

def mcnemar(b, c):
    """b = old pass/new fail, c = old fail/new pass. Returns (statistic, p_value)."""
    if b + c == 0: return (0.0, 1.0)
    stat = (abs(b-c)-1)**2 / (b+c)  # continuity-corrected
    return (stat, _chi2_sf(stat, 1))

def ci_gate(old_pass_rate, new_pass_rate, max_drop_points=7.0):
    """Block if pass rate dropped by more than max_drop_points (percentage points)."""
    drop = (old_pass_rate - new_pass_rate) * 100.0
    return {"blocked": drop > max_drop_points, "drop_points": drop, "threshold_points": max_drop_points}
