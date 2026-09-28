"""
Score Utilities for Interview Coach
"""

from typing import Dict, List, Optional, Union
import logging

logger = logging.getLogger(__name__)


def calculate_weighted_score(
    scores: Dict[str, float],
    weights: Optional[Dict[str, float]] = None
) -> float:
    """Calculate weighted average score"""
    if not scores:
        return 0.0
    
    # Use equal weights if not provided
    if weights is None:
        weights = {key: 1.0 for key in scores}
    
    total_weight = sum(weights.values())
    if total_weight == 0:
        return 0.0
    
    weighted_sum = sum(scores[key] * weights.get(key, 0) for key in scores)
    
    return weighted_sum / total_weight


def normalize_score(score: float, min_val: float = 0.0, max_val: float = 100.0) -> float:
    """Normalize score to 0-100 range"""
    if min_val == max_val:
        return 50.0  # Default middle value
    
    # Clamp the score to the range
    score = max(min_val, min(score, max_val))
    
    # Normalize to 0-100
    return ((score - min_val) / (max_val - min_val)) * 100.0


def calculate_percentage_improvement(old_score: float, new_score: float) -> float:
    """Calculate percentage improvement"""
    if old_score == 0:
        return 0.0
    
    return ((new_score - old_score) / old_score) * 100.0


def calculate_average(scores: List[float]) -> float:
    """Calculate average of scores"""
    if not scores:
        return 0.0
    
    return sum(scores) / len(scores)


def calculate_median(scores: List[float]) -> float:
    """Calculate median of scores"""
    if not scores:
        return 0.0
    
    sorted_scores = sorted(scores)
    n = len(sorted_scores)
    mid = n // 2
    
    if n % 2 == 0:
        return (sorted_scores[mid - 1] + sorted_scores[mid]) / 2
    else:
        return sorted_scores[mid]


def calculate_std_deviation(scores: List[float]) -> float:
    """Calculate standard deviation of scores"""
    if not scores or len(scores) < 2:
        return 0.0
    
    mean = calculate_average(scores)
    variance = sum((x - mean) ** 2 for x in scores) / len(scores)
    
    return variance ** 0.5


def calculate_percentile(scores: List[float], value: float) -> float:
    """Calculate percentile rank of a value in scores"""
    if not scores:
        return 0.0
    
    sorted_scores = sorted(scores)
    count = len(sorted_scores)
    
    # Count how many scores are below the value
    below = sum(1 for s in sorted_scores if s < value)
    equal = sum(1 for s in sorted_scores if s == value)
    
    # Calculate percentile
    percentile = (below + 0.5 * equal) / count * 100
    
    return percentile


def grade_score(score: float) -> str:
    """Convert numeric score to letter grade"""
    if score >= 90:
        return "A+ (Excellent)"
    elif score >= 85:
        return "A (Very Good)"
    elif score >= 80:
        return "A- (Good)"
    elif score >= 75:
        return "B+ (Above Average)"
    elif score >= 70:
        return "B (Average)"
    elif score >= 65:
        return "B- (Below Average)"
    elif score >= 60:
        return "C (Satisfactory)"
    elif score >= 55:
        return "C- (Needs Improvement)"
    elif score >= 50:
        return "D (Poor)"
    else:
        return "F (Fail)"


def score_to_color(score: float) -> str:
    """Convert score to color name"""
    if score >= 90:
        return "success"
    elif score >= 80:
        return "primary"
    elif score >= 70:
        return "info"
    elif score >= 60:
        return "warning"
    else:
        return "danger"


def calculate_composite_score(
    component_scores: Dict[str, float],
    component_weights: Dict[str, float]
) -> Dict[str, Union[float, str]]:
    """Calculate composite score with components"""
    weighted_score = calculate_weighted_score(component_scores, component_weights)
    
    return {
        'overall_score': round(weighted_score, 2),
        'grade': grade_score(weighted_score),
        'color': score_to_color(weighted_score),
        'components': {k: round(v, 2) for k, v in component_scores.items()}
    }


def score_trend(history: List[float]) -> str:
    """Determine score trend from history"""
    if not history or len(history) < 2:
        return "stable"
    
    # Calculate linear regression slope
    n = len(history)
    x = list(range(n))
    y = history
    
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(xi * yi for xi, yi in zip(x, y))
    sum_x2 = sum(xi ** 2 for xi in x)
    
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
    
    if slope > 0.5:
        return "improving"
    elif slope < -0.5:
        return "declining"
    else:
        return "stable"
