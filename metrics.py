# metrics.py
from radon.complexity import cc_visit
from radon.metrics import mi_visit
from radon.visitors import Function

def analyze_metrics(code):
    complexity_scores = cc_visit(code)
    mi_score = mi_visit(code, True)

    cc_total = sum(c.complexity for c in complexity_scores if isinstance(c, Function))
    cc_count = len([c for c in complexity_scores if isinstance(c, Function)])
    avg_cc = cc_total / cc_count if cc_count else 0

    return {
        "maintainability_index": round(mi_score, 2),
        "average_cyclomatic_complexity": round(avg_cc, 2)
    }
