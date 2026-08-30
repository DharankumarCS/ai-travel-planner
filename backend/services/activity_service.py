"""
Activity recommendation service for the travel planner backend.
Rule-based recommendation engine matching travel interests to curated activities.
"""

from typing import List, Dict, Any

# Predefined dataset of activities grouped by interest category
ACTIVITY_DATABASE: Dict[str, List[Dict[str, Any]]] = {
    "food": [
        {
            "name": "Local Street Food & Night Market Tour",
            "category": "food",
            "estimated_cost": "$25 - $40",
            "duration": "2.5 hours",
        },
        {
            "name": "Hands-on Traditional Cooking Masterclass",
            "category": "food",
            "estimated_cost": "$50 - $75",
            "duration": "3 hours",
        },
        {
            "name": "Artisanal Coffee & Pastry Tasting Walk",
            "category": "food",
            "estimated_cost": "$15 - $25",
            "duration": "1.5 hours",
        },
        {
            "name": "Sunset Rooftop Wine & Tapas Experience",
            "category": "food",
            "estimated_cost": "$45 - $65",
            "duration": "2 hours",
        },
        {
            "name": "Historic Farmers Market & Food Hall Discovery",
            "category": "food",
            "estimated_cost": "$10 - $20",
            "duration": "2 hours",
        },
    ],
    "adventure": [
        {
            "name": "Scenic Mountain Trail Hiking & Summit View",
            "category": "adventure",
            "estimated_cost": "$0 - $15",
            "duration": "4 hours",
        },
        {
            "name": "Coastal Kayaking & Sea Cave Exploration",
            "category": "adventure",
            "estimated_cost": "$40 - $60",
            "duration": "3 hours",
        },
        {
            "name": "Canopy Zip-lining & Suspension Bridge Trek",
            "category": "adventure",
            "estimated_cost": "$55 - $80",
            "duration": "2.5 hours",
        },
        {
            "name": "Guided Off-Road Bike & Forest Expedition",
            "category": "adventure",
            "estimated_cost": "$35 - $50",
            "duration": "3 hours",
        },
        {
            "name": "Whitewater Rafting / River Adventure",
            "category": "adventure",
            "estimated_cost": "$60 - $90",
            "duration": "3.5 hours",
        },
    ],
    "culture": [
        {
            "name": "Historic Old Town & Heritage Walking Tour",
            "category": "culture",
            "estimated_cost": "$15 - $30",
            "duration": "2.5 hours",
        },
        {
            "name": "National Museum of Art & History Guided Tour",
            "category": "culture",
            "estimated_cost": "$20 - $35",
            "duration": "3 hours",
        },
        {
            "name": "Ancient Temple & Sacred Architecture Visit",
            "category": "culture",
            "estimated_cost": "$10 - $20",
            "duration": "2 hours",
        },
        {
            "name": "Traditional Folk Music & Cultural Dance Performance",
            "category": "culture",
            "estimated_cost": "$30 - $50",
            "duration": "2 hours",
        },
        {
            "name": "Artisan Craft & Pottery Workshop",
            "category": "culture",
            "estimated_cost": "$25 - $45",
            "duration": "2 hours",
        },
    ],
    "relaxation": [
        {
            "name": "Thermal Bath & Herbal Spa Wellness Session",
            "category": "relaxation",
            "estimated_cost": "$40 - $70",
            "duration": "2.5 hours",
        },
        {
            "name": "Botanical Gardens Leisure Stroll & Tea Room",
            "category": "relaxation",
            "estimated_cost": "$10 - $20",
            "duration": "2 hours",
        },
        {
            "name": "Golden Hour Sunset Harbor Cruise",
            "category": "relaxation",
            "estimated_cost": "$35 - $55",
            "duration": "1.5 hours",
        },
        {
            "name": "Scenic Waterfront Promenade & Cafe Lounging",
            "category": "relaxation",
            "estimated_cost": "$10 - $15",
            "duration": "2 hours",
        },
        {
            "name": "Mindful Yoga & Meditation in the Park",
            "category": "relaxation",
            "estimated_cost": "$15 - $25",
            "duration": "1 hour",
        },
    ],
}


def get_recommended_activities(
    destination: str = "",
    interests: List[str] = None,
    min_count: int = 5,
    max_count: int = 8,
) -> List[Dict[str, Any]]:
    """
    Recommends 5-8 activities matching the user's travel interests and destination.

    Args:
        destination (str): Name of destination (optional context).
        interests (List[str]): List of interest categories (e.g. ['food', 'adventure', 'culture', 'relaxation']).
        min_count (int): Minimum number of activities to return (default: 5).
        max_count (int): Maximum number of activities to return (default: 8).

    Returns:
        List[Dict[str, Any]]: List of matching activity dictionaries with
        name, category, estimated_cost, and duration.
    """
    if not interests:
        interests = ["culture", "food", "relaxation", "adventure"]

    # Normalize category names
    cleaned_interests = [i.strip().lower() for i in interests if isinstance(i, str)]
    if not cleaned_interests:
        cleaned_interests = ["culture", "food", "relaxation", "adventure"]

    matched_activities: List[Dict[str, Any]] = []
    seen_names = set()

    # Step 1: Collect activities from requested categories
    max_items_per_category = max(2, (max_count // len(cleaned_interests)) + 1)

    for interest in cleaned_interests:
        activities = ACTIVITY_DATABASE.get(interest, [])
        for act in activities[:max_items_per_category]:
            if act["name"] not in seen_names:
                matched_activities.append(act)
                seen_names.add(act["name"])

    # Step 2: Backfill if fewer than min_count
    if len(matched_activities) < min_count:
        for category, activities in ACTIVITY_DATABASE.items():
            for act in activities:
                if act["name"] not in seen_names:
                    matched_activities.append(act)
                    seen_names.add(act["name"])
                if len(matched_activities) >= min_count:
                    break
            if len(matched_activities) >= min_count:
                break

    # Step 3: Trim to max_count (5-8 items)
    final_recommendations = matched_activities[:max_count]

    # Add destination tag if provided
    formatted_recommendations = []
    for act in final_recommendations:
        item = act.copy()
        if destination and destination.strip():
            item["destination"] = destination.strip().title()
        formatted_recommendations.append(item)

    return formatted_recommendations