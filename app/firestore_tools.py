"""Firestore database tools for FitCoach AI.

Provides function tools to read and write exercise library items and workout logs.
"""

import datetime
from google.cloud import firestore

# IMPORTANT: Hardcode GCP Project ID as a string.
# On Agent Platform, google.auth.default() or GOOGLE_CLOUD_PROJECT return project number,
# which breaks Firestore after deployment.
PROJECT_ID = "qwiklabs-gcp-02-0ea6d4bc8e38"


def _get_firestore_client() -> firestore.Client:
    """Returns a Firestore client initialized with hardcoded project ID."""
    return firestore.Client(project=PROJECT_ID)


def search_exercises(category: str = "") -> str:
    """Searches or lists exercises from the exercise library in Firestore.

    Args:
        category: Optional category filter (e.g. "Push", "Pull", "Legs", "Back", "Chest", "Shoulders").

    Returns:
        A formatted string summary of matching exercises.
    """
    db = _get_firestore_client()
    collection_ref = db.collection("exercises")
    docs = list(collection_ref.stream())

    if not docs:
        return "No exercises found in the database."

    results = []
    category_lower = category.lower().strip()

    for doc in docs:
        data = doc.to_dict()
        doc_category = data.get("category", "")
        doc_name = data.get("name", doc.id)

        if category_lower and category_lower not in doc_category.lower() and category_lower not in doc_name.lower():
            continue

        target_muscles = ", ".join(data.get("target_muscles", []))
        results.append(
            f"• {doc_name} [{doc_category}]\n"
            f"  Difficulty: {data.get('difficulty', 'N/A')} | "
            f"Target: {target_muscles}\n"
            f"  Sets/Reps: {data.get('recommended_sets', 3)} sets x {data.get('recommended_reps', 10)} reps\n"
            f"  Description: {data.get('description', '')}"
        )

    if not results:
        return f"No exercises found matching category or filter '{category}'."

    return "Found Exercises:\n\n" + "\n\n".join(results)


def get_exercise_details(exercise_name: str) -> str:
    """Retrieves full details for a specific exercise from Firestore.

    Args:
        exercise_name: The name or key of the exercise to look up (e.g. "Barbell Bench Press", "squat").

    Returns:
        Formatted details about the exercise.
    """
    db = _get_firestore_client()
    collection_ref = db.collection("exercises")
    docs = list(collection_ref.stream())

    query_lower = exercise_name.lower().strip()
    for doc in docs:
        data = doc.to_dict()
        name = data.get("name", "")
        if query_lower in name.lower() or query_lower in doc.id.lower():
            target_muscles = ", ".join(data.get("target_muscles", []))
            return (
                f"Exercise: {name}\n"
                f"Category: {data.get('category', 'General')}\n"
                f"Difficulty: {data.get('difficulty', 'N/A')}\n"
                f"Target Muscles: {target_muscles}\n"
                f"Recommended Volume: {data.get('recommended_sets', 3)} sets x {data.get('recommended_reps', 10)} reps\n"
                f"Description: {data.get('description', '')}"
            )

    return f"Exercise '{exercise_name}' was not found in the Firestore database."


def add_exercise(
    name: str,
    category: str,
    target_muscles: str,
    recommended_sets: int = 3,
    recommended_reps: int = 10,
    difficulty: str = "Intermediate",
    description: str = "",
) -> str:
    """Adds a new exercise item into the Firestore exercise database.

    Args:
        name: Name of the exercise (e.g., "Incline Dumbbell Press").
        category: Exercise category (e.g., "Chest / Push").
        target_muscles: Comma-separated list of target muscles (e.g., "Upper Chest, Triceps").
        recommended_sets: Number of recommended sets (e.g., 3).
        recommended_reps: Number of recommended reps per set (e.g., 10).
        difficulty: Difficulty level ("Beginner", "Intermediate", "Advanced").
        description: Description of proper form and execution.

    Returns:
        Confirmation message.
    """
    db = _get_firestore_client()
    doc_id = name.lower().replace(" ", "-").replace("/", "-")
    muscles_list = [m.strip() for m in target_muscles.split(",") if m.strip()]

    doc_data = {
        "name": name,
        "category": category,
        "target_muscles": muscles_list,
        "recommended_sets": recommended_sets,
        "recommended_reps": recommended_reps,
        "difficulty": difficulty,
        "description": description,
    }

    db.collection("exercises").document(doc_id).set(doc_data)
    return f"Successfully added '{name}' to Firestore under category '{category}'."


def log_workout(
    exercise_name: str,
    sets: int,
    reps: int,
    weight_lbs: float,
    notes: str = "",
) -> str:
    """Logs a completed workout entry into the Firestore 'workout_logs' collection.

    Args:
        exercise_name: Name of the exercise performed (e.g. "Barbell Bench Press").
        sets: Number of sets completed.
        reps: Repetitions per set.
        weight_lbs: Weight used in pounds (0 for bodyweight).
        notes: Optional notes or observations about the set/workout.

    Returns:
        Confirmation message.
    """
    db = _get_firestore_client()
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

    log_entry = {
        "exercise_name": exercise_name,
        "sets": sets,
        "reps": reps,
        "weight_lbs": weight_lbs,
        "notes": notes,
        "timestamp": timestamp,
    }

    doc_ref = db.collection("workout_logs").document()
    doc_ref.set(log_entry)

    return (
        f"Logged workout successfully!\n"
        f"Exercise: {exercise_name} | {sets} sets x {reps} reps @ {weight_lbs} lbs\n"
        f"Log ID: {doc_ref.id}"
    )


def get_workout_history(limit: int = 5) -> str:
    """Retrieves recent workout logs from the Firestore 'workout_logs' collection.

    Args:
        limit: Number of recent logs to fetch (default: 5).

    Returns:
        Formatted summary of recent workout history.
    """
    db = _get_firestore_client()
    docs = list(db.collection("workout_logs").stream())

    if not docs:
        return "No workout logs found in history."

    # Sort manually by timestamp descending
    logs = [d.to_dict() for d in docs]
    logs.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    logs = logs[:limit]

    formatted_logs = []
    for entry in logs:
        ts = entry.get("timestamp", "")[:19].replace("T", " ")
        formatted_logs.append(
            f"• [{ts}] {entry.get('exercise_name', 'Workout')}: "
            f"{entry.get('sets')} sets x {entry.get('reps')} reps @ {entry.get('weight_lbs')} lbs"
            + (f" ({entry.get('notes')})" if entry.get("notes") else "")
        )

    return "Recent Workout History:\n" + "\n".join(formatted_logs)
