"""Fitness recipe and meal search tools using TheMealDB public API."""

import os
import requests


def search_fitness_recipes(query: str) -> str:
    """Searches for healthy recipes and meal ideas matching a search term from TheMealDB public API.

    Args:
        query: Search term for ingredients or meal types (e.g. "chicken", "salmon", "egg", "salad").

    Returns:
        Formatted summary of matching recipes, ingredients, and instructions.
    """
    api_key = os.environ.get("MEALDB_API_KEY", "1")
    url = f"https://www.themealdb.com/api/json/v1/{api_key}/search.php"

    try:
        response = requests.get(url, params={"s": query}, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        return f"Error fetching recipes from TheMealDB API: {e}"

    meals = data.get("meals")
    if not meals:
        return f"No recipe ideas found matching '{query}'."

    results = []
    for meal in meals[:3]:  # Top 3 recipe matches
        name = meal.get("strMeal", "Meal")
        category = meal.get("strCategory", "General")
        area = meal.get("strArea", "International")
        instructions = meal.get("strInstructions", "").strip()
        if len(instructions) > 250:
            instructions = instructions[:250] + "..."

        # Extract primary ingredients
        ingredients = []
        for i in range(1, 15):
            ing = meal.get(f"strIngredient{i}")
            measure = meal.get(f"strMeasure{i}")
            if ing and ing.strip():
                measure_str = f" ({measure.strip()})" if measure and measure.strip() else ""
                ingredients.append(f"{ing.strip()}{measure_str}")

        ing_text = ", ".join(ingredients[:6]) if ingredients else "See instructions"

        results.append(
            f"🥗 {name} [{category} - {area}]\n"
            f"  Key Ingredients: {ing_text}\n"
            f"  Instructions: {instructions}"
        )

    return f"Recipe Recommendations for '{query}':\n\n" + "\n\n".join(results)
