from pathlib import Path

from preprocessor.core.image_transform import ImageTransform, ImageTransformWorkItem
from preprocessor.core.message_reporter import MessageReporter, NoopMessageReporter
from preprocessor.core.photo_params import PhotoParams
from preprocessor.core.progress_reporter import ProgressReporter, NoopProgressReporter, WeightedSubProgressReporter
from preprocessor.core.types import ImageRGB


def process_image(
    input_path: Path,
    params: PhotoParams,
    output_path: Path | None,
    transforms: list[ImageTransform],
    messages: MessageReporter = NoopMessageReporter(),
    progress: ProgressReporter = NoopProgressReporter(),
) -> ImageRGB | None:
    """Process an image with the given transforms and export it to the output path, if given.

    :param input_path: The path to the input image file.
    :param params: The parameters used for processing this image, e.g. quadrat corners.
    :param output_path: The path to the output image file. If None, the processed image will not be saved to disk.
    :param transforms: The list of transforms to apply to the image, in order.
    Each transform will receive the output of the previous transform as input.
    :param messages: A message reporter for reporting messages during processing of this image.
    If not provided, a no-op message reporter will be used.
    :param progress: A progress reporter for reporting progress of processing steps.
    If not provided, a no-op progress reporter will be used.
    :return: The final processed image after applying all transforms; or None when processing failed.
    """

    # Read the image
    image_id = input_path.stem  # FIXME: This might not be unique
    img: ImageRGB
    try:
        img = ImageRGB.from_file(input_path)
    except Exception as e:
        messages.error(
            "image_load_failed",
            f"Failed to load image from {input_path}: {e!s}",
            step="load_image",
            image_id=image_id,
        )
        return None

    item = ImageTransformWorkItem(
        image_id=image_id,
        image_path=input_path,
        image=img,
        params=params,
    )

    # Apply transforms in order
    for i, transform in enumerate(transforms):
        try:
            sub_progress = WeightedSubProgressReporter(
                progress,
                start=1.0 * i / len(transforms),
                weight=1.0 / len(transforms),
                image_id=image_id,
                step=transform.name,
            )
            item = transform(item, messages=messages, progress=sub_progress)
        except Exception as e:
            messages.error(
                "transform_failed",
                f"Transform '{transform.name}' failed: {e!s}",
                step=transform.name,
                image_id=image_id,
            )
            return None

    # Export the final image if output path is given
    if output_path is not None:
        try:
            item.image.to_file(output_path)
        except Exception as e:
            messages.error(
                "image_save_failed",
                f"Failed to save image to {output_path}: {e!s}",
                step="save_image",
                image_id=image_id,
            )
            return None

    # Return the final image
    return item.image