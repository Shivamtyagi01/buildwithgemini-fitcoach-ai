"""Image generation and Cloud Storage upload tools for FitCoach AI."""

import uuid
from google import genai
from google.adk.tools import ToolContext
from google.cloud import storage
from google.genai import types

# IMPORTANT: Hardcode GCP Project ID and Bucket Name as strings.
# On Agent Platform, google.auth.default() or GOOGLE_CLOUD_PROJECT return project number,
# which breaks GCP SDK client calls after deployment.
PROJECT_ID = "qwiklabs-gcp-02-0ea6d4bc8e38"
BUCKET_NAME = "fitcoach-ai-media-qwiklabs-gcp-02-0ea6d4bc8e38"


async def generate_workout_badge_image(
    achievement_description: str,
    tool_context: ToolContext,
) -> str:
    """Generates a custom visual workout achievement badge using gemini-3.1-flash-lite-image model,
    saves it as an artifact in Playground, uploads it to public Cloud Storage, and returns its public HTTPS URL.

    Args:
        achievement_description: Description of the workout milestone, PR, or exercise achievement (e.g. "Bench Press 225 lbs PR", "100 Pushups Mastered").
        tool_context: ADK ToolContext provided automatically by the ADK runtime.

    Returns:
        Public HTTPS URL of the uploaded image in Google Cloud Storage.
    """
    # 1. Initialize GenAI client in global region
    genai_client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location="global",
    )

    prompt = (
        f"A modern, vibrant, high-quality fitness achievement badge and poster celebrating: "
        f"'{achievement_description}'. Sleek athletic typography, bold colors, dark theme."
    )

    response = genai_client.models.generate_content(
        model="gemini-3.1-flash-lite-image",
        contents=prompt,
        config=types.GenerateContentConfig(response_modalities=["IMAGE"]),
    )

    image_bytes = None
    mime_type = "image/png"

    if response.candidates and response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                image_bytes = part.inline_data.data
                if part.inline_data.mime_type:
                    mime_type = part.inline_data.mime_type
                break

    if not image_bytes:
        return "Error: Image generation failed or returned no image data."

    ext = "png" if "png" in mime_type.lower() else "jpg"
    filename = f"badge_{uuid.uuid4().hex[:8]}.{ext}"

    # 2. Save image artifact with tool_context so it appears in Playground Artifacts panel
    artifact = types.Part.from_bytes(data=image_bytes, mime_type=mime_type)
    await tool_context.save_artifact(filename=filename, artifact=artifact)

    # 3. Upload image bytes directly to public GCS bucket
    storage_client = storage.Client(project=PROJECT_ID)
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(filename)
    blob.upload_from_string(image_bytes, content_type=mime_type)

    # 4. Return public HTTPS URL
    public_url = f"https://storage.googleapis.com/{BUCKET_NAME}/{filename}"
    return f"Generated Workout Badge!\nArtifact: {filename}\nPublic Image URL: {public_url}"
