#!/usr/bin/env python3
"""Seed script for FitCoach AI Firestore database.

Seeds exercise collection with initial exercise library items.
"""

from google.cloud import firestore

# IMPORTANT: Hardcode GCP Project ID as a string.
# On Agent Platform, google.auth.default() or GOOGLE_CLOUD_PROJECT return project number,
# which breaks Firestore after deployment.
PROJECT_ID = "qwiklabs-gcp-02-0ea6d4bc8e38"


def seed_database():
    """Seeds default exercises into Firestore."""
    db = firestore.Client(project=PROJECT_ID)
    collection_ref = db.collection("exercises")

    seed_exercises = [
        {
            "id": "barbell-bench-press",
            "name": "Barbell Bench Press",
            "category": "Chest / Push",
            "target_muscles": ["Pectoralis Major", "Triceps Brachii", "Anterior Deltoid"],
            "recommended_sets": 4,
            "recommended_reps": 8,
            "difficulty": "Intermediate",
            "description": "Classic upper-body compound movement focusing on chest strength and hypertrophy.",
        },
        {
            "id": "barbell-squat",
            "name": "Barbell Back Squat",
            "category": "Legs / Lower Body",
            "target_muscles": ["Quadriceps", "Gluteus Maximus", "Hamstrings", "Core"],
            "recommended_sets": 4,
            "recommended_reps": 6,
            "difficulty": "Intermediate",
            "description": "Fundamental lower-body compound exercise targeting quads, glutes, and core stability.",
        },
        {
            "id": "conventional-deadlift",
            "name": "Conventional Deadlift",
            "category": "Back / Pull",
            "target_muscles": ["Erector Spinae", "Hamstrings", "Gluteus Maximus", "Latissimus Dorsi"],
            "recommended_sets": 3,
            "recommended_reps": 5,
            "difficulty": "Advanced",
            "description": "Full posterior chain pull movement building raw strength and back density.",
        },
        {
            "id": "dumbbell-overhead-press",
            "name": "Dumbbell Overhead Shoulder Press",
            "category": "Shoulders / Push",
            "target_muscles": ["Anterior Deltoid", "Lateral Deltoid", "Triceps"],
            "recommended_sets": 3,
            "recommended_reps": 10,
            "difficulty": "Beginner",
            "description": "Seated or standing press focusing on shoulder development and overhead stability.",
        },
        {
            "id": "pull-ups",
            "name": "Bodyweight Pull-Ups",
            "category": "Back / Pull",
            "target_muscles": ["Latissimus Dorsi", "Biceps Brachii", "Rhomboids"],
            "recommended_sets": 3,
            "recommended_reps": 8,
            "difficulty": "Intermediate",
            "description": "Calisthenic pulling movement for back width and arm strength.",
        },
    ]

    print(f"Seeding Firestore collection 'exercises' in project '{PROJECT_ID}'...")
    for exercise in seed_exercises:
        doc_id = exercise["id"]
        doc_data = {k: v for k, v in exercise.items() if k != "id"}
        collection_ref.document(doc_id).set(doc_data)
        print(f"  ✓ Seeded: {exercise['name']} ({doc_id})")

    print("\n✅ Firestore seeding complete!")


if __name__ == "__main__":
    seed_database()
