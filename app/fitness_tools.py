"""Fitness computation tools for FitCoach AI.

Provides calculation tools for One-Rep Max (1RM) and strength training intensity zones.
"""


def calculate_1rm_and_zones(weight_lbs: float, reps: int) -> str:
    """Calculates the estimated One-Rep Max (1RM) and strength training intensity zones.

    Args:
        weight_lbs: The weight lifted in pounds (must be greater than 0).
        reps: The number of repetitions performed (must be between 1 and 30).

    Returns:
        A formatted summary containing estimated 1RM and percentage training zones.
    """
    if weight_lbs <= 0 or reps <= 0:
        return "Error: Weight and reps must be positive numbers."

    if reps == 1:
        one_rm = weight_lbs
    else:
        # Epley Formula: 1RM = weight * (1 + reps / 30)
        # Brzycki Formula: 1RM = weight * (36 / (37 - reps))
        epley = weight_lbs * (1 + reps / 30.0)
        brzycki = weight_lbs * (36.0 / (37.0 - min(reps, 36)))
        one_rm = (epley + brzycki) / 2.0

    one_rm_round = round(one_rm, 1)

    zones = {
        "Heavy Strength (90%)": round(one_rm * 0.90, 1),
        "Hypertrophy Zone (75-85%)": f"{round(one_rm * 0.75, 1)} - {round(one_rm * 0.85, 1)} lbs",
        "Endurance / Speed Zone (60-70%)": f"{round(one_rm * 0.60, 1)} - {round(one_rm * 0.70, 1)} lbs",
        "Warm-up / Recovery (50%)": round(one_rm * 0.50, 1),
    }

    lines = [
        f"📊 1-Rep Max (1RM) Calculation for {weight_lbs} lbs x {reps} reps:",
        f"  • Estimated 1RM: {one_rm_round} lbs",
        "\n💪 Recommended Training Intensity Zones:",
        f"  • Heavy Strength (90% 1RM): {zones['Heavy Strength (90%)']} lbs (1-3 reps)",
        f"  • Hypertrophy Zone (75-85% 1RM): {zones['Hypertrophy Zone (75-85%)']} (6-12 reps)",
        f"  • Endurance / Speed Zone (60-70% 1RM): {zones['Endurance / Speed Zone (60-70%)']} (12-20 reps)",
        f"  • Warm-up / Recovery (50% 1RM): {zones['Warm-up / Recovery (50%)']} lbs",
    ]

    return "\n".join(lines)
