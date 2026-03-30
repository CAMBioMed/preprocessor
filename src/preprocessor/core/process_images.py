from pathlib import Path

from preprocessor.core.image_transform import ImageTransform, ImageTransformWorkItem
from preprocessor.core.types import ImageRGB


def process_and_export_image(
    input_path: Path,
    output_path: Path,
    transforms: list[ImageTransform],
) -> ImageTransformWorkItem:
    """Process an image with the given transforms and export it to the output path."""

    # Read the image
    item = ImageTransformWorkItem(
        image_id=input_path.stem,
        image_path=input_path,
        image=None,  # type: ignore[assignment]
        params=None,  # type: ignore[assignment]
    )
    try:
        item.image = ImageRGB.from_file(input_path)
    except Exception as e:
        item.error(
            code="image_load_failed",
            text=f"Failed to load image from {input_path}: {e}",
            step="load_image",
        )
        return item