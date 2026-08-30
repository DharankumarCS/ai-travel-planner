"""
AI Itinerary Generation Service using Google Gemini.
Generates structured day-by-day travel plans using gemini-1.5-flash.
"""

import os
import json
import re
from typing import List, Dict, Any, Union
from dotenv import load_dotenv, find_dotenv
import google.generativeai as genai

# Load environment variables from .env file
load_dotenv(find_dotenv())

# Get Gemini API key and configure client if available
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)


def generate_itinerary(
    destination: str,
    num_days: int,
    interests: Union[List[str], str] = None,
) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Generates a day-by-day travel itinerary using Gemini 1.5 Flash.

    Args:
        destination (str): Target travel destination.
        num_days (int): Number of trip days.
        interests (List[str] or str): Traveler's interests (e.g. food, culture, adventure).

    Returns:
        List[Dict[str, Any]] | Dict[str, Any]: List of itinerary days or error dictionary.
    """
    try:
        # Re-check API key in case it was loaded or updated at runtime
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            load_dotenv(find_dotenv())
            api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            return {
                "error": "AI generation failed",
                "details": "GEMINI_API_KEY is missing. Please configure GEMINI_API_KEY in your .env file."
            }

        # Configure genai with the active key
        genai.configure(api_key=api_key)

        # Format interests string
        if isinstance(interests, list):
            interests_str = ", ".join(interests) if interests else "general sightseeing, local culture, food"
        elif isinstance(interests, str) and interests.strip():
            interests_str = interests.strip()
        else:
            interests_str = "general sightseeing, local culture, food"

        # Build prompt requesting strict JSON response
        prompt = f"""You are an expert travel planner.
Create a personalized day-by-day travel itinerary for {destination} for {num_days} days based on these interests: {interests_str}.

Respond ONLY in valid JSON format (a JSON array of objects). Do not include any explanations, markdown headers, or commentary outside the JSON array.

Strict schema to follow:
[
  {{
    "day": 1,
    "title": "Descriptive title for Day 1",
    "morning": "Detailed morning activity description",
    "afternoon": "Detailed afternoon activity description",
    "evening": "Detailed evening activity description"
  }}
]
"""

        # Call Gemini model
        model = genai.GenerativeModel("gemini-3.6-flash")
        response = model.generate_content(prompt)

        raw_text = response.text.strip() if response and response.text else ""
        if not raw_text:
            return {
                "error": "AI generation failed",
                "details": "Received empty response from Gemini."
            }

        # Strip markdown code fences (e.g. ```json ... ``` or ``` ... ```)
        cleaned_text = raw_text
        if cleaned_text.startswith("```json"):
            cleaned_text = cleaned_text[7:]
        elif cleaned_text.startswith("```"):
            cleaned_text = cleaned_text[3:]
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text[:-3]
        cleaned_text = cleaned_text.strip()

        # Parse JSON
        parsed_itinerary = json.loads(cleaned_text)

        if not isinstance(parsed_itinerary, list):
            return {
                "error": "AI generation failed",
                "details": f"Expected a JSON list of days, but got {type(parsed_itinerary).__name__}."
            }

        return parsed_itinerary

    except Exception as e:
        return {
            "error": "AI generation failed",
            "details": str(e)
        }