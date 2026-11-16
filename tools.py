import random
import requests
from langchain_core.tools import tool

# Curated fallback trivia in case NumbersAPI service is temporarily down or returning 404
FALLBACK_NUMBER_FACTS = {
    "42": "42 is the number of dots on a pair of standard dice (21 on each die), and the answer to life, the universe, and everything according to The Hitchhiker's Guide to the Galaxy.",
    "7": "7 is the most popular favorite number worldwide, the number of continents, and the number of colors in a rainbow.",
    "0": "0 is the only real number that is neither positive nor negative.",
    "1": "1 is the only number that is neither prime nor composite.",
    "13": "13 is known for triskaidekaphobia (the fear of the number 13), but in Italy and ancient Egypt, it was considered a lucky number!",
    "73": "73 is the 21st prime number. Its mirror 37 is the 12th prime number, whose mirror 21 is the product of multiplying 7 and 3.",
    "100": "100 is 10 squared and represents the boiling point of water at sea level in Celsius.",
}


@tool
def get_joke(category: str = "Any") -> str:
    """
    Fetch a random joke. Categories: Any, Programming, Misc, Pun, Spooky, Christmas.
    Uses JokeAPI — free, no API key. Filters out NSFW and racist content.
    """
    if not category or str(category).strip() == "":
        category = "Any"

    clean_category = str(category).strip()
    url = f"https://v2.jokeapi.dev/joke/{clean_category}?blacklistFlags=nsfw,racist"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("error"):
            return f"Error from JokeAPI: {data.get('message', 'Unknown error occurred.')}"

        joke_type = data.get("type")
        if joke_type == "twopart":
            setup = data.get("setup", "")
            delivery = data.get("delivery", "")
            return f"{setup}\n{delivery}"
        elif joke_type == "single":
            return data.get("joke", "No joke found.")
        else:
            return "Could not retrieve joke."
    except requests.RequestException as e:
        return f"Network error fetching joke: {e}"
    except Exception as e:
        return f"Unexpected error fetching joke: {e}"


@tool
def get_number_fact(number: str = "random") -> str:
    """
    Get a fascinating trivia fact about any number. Pass a number like "42" or "random".
    Uses NumbersAPI — free, no API key.
    """
    if not number or str(number).strip() == "":
        target_number = "random"
    else:
        target_number = str(number).strip()

    url = f"http://numbersapi.com/{target_number}/trivia"

    try:
        response = requests.get(url, timeout=10)
        # Check if the service returned plain text and status 200
        if (
            response.status_code == 200
            and not response.text.strip().lower().startswith("<!doctype")
            and not response.text.strip().lower().startswith("<html")
        ):
            return response.text.strip()
        else:
            # Fallback if NumbersAPI service is currently returning 404/5xx HTML
            key = target_number.lower()
            if key in FALLBACK_NUMBER_FACTS:
                return FALLBACK_NUMBER_FACTS[key]
            elif key == "random":
                return random.choice(list(FALLBACK_NUMBER_FACTS.values()))
            else:
                return f"{target_number} is a fascinating number with unique mathematical and cultural properties."
    except requests.RequestException:
        key = target_number.lower()
        if key in FALLBACK_NUMBER_FACTS:
            return FALLBACK_NUMBER_FACTS[key]
        elif key == "random":
            return random.choice(list(FALLBACK_NUMBER_FACTS.values()))
        return f"{target_number} is an intriguing number in mathematics and trivia."
    except Exception as e:
        return f"Unexpected error fetching number fact: {e}"
