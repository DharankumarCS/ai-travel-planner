"""
Travel planning routes for the FastAPI backend.
Generates full travel plans including itinerary, packing checklist,
budget breakdown, and recommended activities.
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from services.budget_service import calculate_budget
from services.activity_service import get_recommended_activities
from services.itinerary_service import generate_itinerary

router = APIRouter(tags=["Travel Planner"])


class TravelPlanRequest(BaseModel):
    destination: str = Field(..., description="Destination city or country")
    num_days: int = Field(default=3, ge=1, le=30, description="Number of days for the trip")
    total_budget: float = Field(default=1000.0, ge=0, description="Total budget in USD")
    interests: List[str] = Field(
        default=["culture", "food"],
        description="List of interests such as food, adventure, culture, relaxation"
    )


def generate_packing_checklist(destination: str, num_days: int, interests: List[str]) -> List[str]:
    """Generates a contextual packing checklist based on trip length and interests."""
    checklist = [
        "Passport / ID and travel tickets",
        "Credit cards, emergency cash, and travel insurance",
        "Phone, universal power adapter, and portable charger",
        "Daily medications and compact first-aid kit",
        f"{min(num_days + 1, 7)}x comfortable weather-appropriate outfits",
        "Toiletries and personal care essentials",
    ]

    interests_lower = [i.lower() for i in interests]

    if "adventure" in interests_lower:
        checklist.extend(["Sturdy hiking shoes", "Refillable water bottle", "Lightweight rain jacket / windbreaker"])
    if "food" in interests_lower:
        checklist.extend(["Digestive aids / antacids", "Reusable cutlery / tote bag for markets"])
    if "culture" in interests_lower:
        checklist.extend(["Modest attire for temples/churches", "Comfortable walking sneakers", "Small daypack"])
    if "relaxation" in interests_lower:
        checklist.extend(["Swimsuit & sunglasses", "Sunscreen & aloe vera", "E-reader or travel book"])

    return list(dict.fromkeys(checklist))  # Preserve order without duplicates


def build_travel_plan(destination: str, num_days: int, total_budget: float, interests: List[str]) -> Dict[str, Any]:
    """Core logic to assemble the full travel plan."""
    # 1. Calculate budget breakdown
    budget_breakdown = calculate_budget(
        total_budget=total_budget,
        num_days=num_days,
        destination=destination,
    )

    # 2. Get rule-based recommended activities matching interests
    recommended_activities = get_recommended_activities(
        destination=destination,
        interests=interests,
        min_count=5,
        max_count=8,
    )

    # 3. Generate AI-powered itinerary using Gemini
    itinerary = generate_itinerary(
        destination=destination,
        num_days=num_days,
        interests=interests,
    )

    # 4. Generate customized packing checklist
    packing_checklist = generate_packing_checklist(
        destination=destination,
        num_days=num_days,
        interests=interests,
    )

    return {
        "destination": destination,
        "num_days": num_days,
        "total_budget": total_budget,
        "interests": interests,
        "budget_breakdown": budget_breakdown,
        "recommended_activities": recommended_activities,
        "itinerary": itinerary,
        "packing_checklist": packing_checklist,
    }


@router.post("/generate-plan")
def generate_plan_post(request: TravelPlanRequest) -> Dict[str, Any]:
    """
    POST endpoint to generate a complete travel plan with budget breakdown,
    recommended activities, itinerary, and packing checklist.
    """
    try:
        return build_travel_plan(
            destination=request.destination,
            num_days=request.num_days,
            total_budget=request.total_budget,
            interests=request.interests,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/generate-plan")
def generate_plan_get(
    destination: str = Query(..., description="Destination city/country"),
    num_days: int = Query(default=3, ge=1, le=30, description="Number of days"),
    total_budget: float = Query(default=1000.0, ge=0, description="Total budget in USD"),
    interests: Optional[List[str]] = Query(
        default=["culture", "food"],
        description="List of travel interests"
    ),
) -> Dict[str, Any]:
    """
    GET endpoint for quick testing and browser access to travel plan generator.
    """
    try:
        return build_travel_plan(
            destination=destination,
            num_days=num_days,
            total_budget=total_budget,
            interests=interests or ["culture", "food"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))