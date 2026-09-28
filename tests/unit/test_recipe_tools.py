"""Unit tests for public recipe search tools."""

from app.recipe_tools import search_fitness_recipes


def test_search_fitness_recipes():
    result = search_fitness_recipes("chicken")
    assert "Recipe Recommendations" in result or "Chicken" in result
    assert "Ingredients" in result
