"""
Budget planning service for the travel planner backend.
Calculates budget breakdown by category and daily average spending.
"""

from typing import Dict, Any


def calculate_budget(total_budget: float, num_days: int, destination: str = "") -> Dict[str, Any]:
    """
    Calculates budget breakdown by category and daily spending average.

    Breakdown rules:
    - Accommodation: 35%
    - Food: 25%
    - Transportation: 15%
    - Activities: 20%
    - Miscellaneous: 5%

    Args:
        total_budget (float): Total trip budget.
        num_days (int): Number of days for the trip.
        destination (str, optional): Destination name. Defaults to "".

    Returns:
        Dict[str, Any]: Budget breakdown and daily averages.
    """
    if total_budget < 0:
        total_budget = 0.0
    if num_days <= 0:
        num_days = 1

    daily_budget = round(total_budget / num_days, 2)

    categories = {
        "accommodation": round(total_budget * 0.35, 2),
        "food": round(total_budget * 0.25, 2),
        "transportation": round(total_budget * 0.15, 2),
        "activities": round(total_budget * 0.20, 2),
        "miscellaneous": round(total_budget * 0.05, 2),
    }

    daily_categories = {
        category: round(amount / num_days, 2)
        for category, amount in categories.items()
    }

    return {
        "destination": destination,
        "total_budget": round(float(total_budget), 2),
        "num_days": num_days,
        "daily_average": daily_budget,
        "categories": categories,
        "daily_categories": daily_categories,
        "percentages": {
            "accommodation": "35%",
            "food": "25%",
            "transportation": "15%",
            "activities": "20%",
            "miscellaneous": "5%",
        },
    }