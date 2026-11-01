import contextvars
from typing import Optional, TypedDict

class CalorieEstimation(TypedDict):
    food_estimations: list[dict]
    assumptions: str
    total_calories: float

_calorie_estimation: contextvars.ContextVar[Optional[list[CalorieEstimation]]] = contextvars.ContextVar("calorie_estimation", default=None)

def start() -> None:
    """Mulai estimasi kalori baru untuk request saat ini."""
    _calorie_estimation.set([])

def add(food_estimations: list[dict], assumptions: str, total_calories: float) -> None:
    """Tambahkan estimasi kalori untuk request saat ini."""
    bucket = _calorie_estimation.get()
    if bucket is None:  
        return

    bucket.append({
        "food_estimations": food_estimations,
        "assumptions": assumptions,
        "total_calories": total_calories
    })

def collect() -> list[CalorieEstimation]:
    """Ambil semua estimasi kalori pada request saat ini."""
    return _calorie_estimation.get() or []