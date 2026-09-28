"""Unit tests for image generation and storage tools."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from app.image_tools import BUCKET_NAME, PROJECT_ID, generate_workout_badge_image


@pytest.mark.asyncio
async def test_generate_workout_badge_image_mock():
    mock_tool_context = MagicMock()
    mock_tool_context.save_artifact = AsyncMock(return_value=1)

    mock_part = MagicMock()
    mock_part.inline_data.data = b"fake_image_data"
    mock_part.inline_data.mime_type = "image/png"

    mock_response = MagicMock()
    mock_response.candidates = [MagicMock(content=MagicMock(parts=[mock_part]))]

    with patch("google.genai.Client") as mock_genai_client, patch("google.cloud.storage.Client") as mock_storage_client:
        mock_genai_instance = MagicMock()
        mock_genai_instance.models.generate_content.return_value = mock_response
        mock_genai_client.return_value = mock_genai_instance

        mock_bucket = MagicMock()
        mock_blob = MagicMock()
        mock_bucket.blob.return_value = mock_blob
        mock_storage_client.return_value.bucket.return_value = mock_bucket

        result = await generate_workout_badge_image("Bench Press 225 lbs", mock_tool_context)

        assert "https://storage.googleapis.com/" in result
        assert BUCKET_NAME in result
        mock_tool_context.save_artifact.assert_called_once()
        mock_blob.upload_from_string.assert_called_once_with(b"fake_image_data", content_type="image/png")
