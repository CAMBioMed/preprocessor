import cv2
import numpy as np

from preprocessor.core.transform.image_transform import ImageTransformWorkItem
from preprocessor.core.message_reporter import MessageReporter, NOOP_MESSAGE_REPORTER
from preprocessor.core.progress_reporter import ProgressReporter, NOOP_PROGRESS_REPORTER
from preprocessor.core.types import ImageRGB


class PerspectiveCropTransform:
    name = "perspective_crop"

    def __call__(
        self,
        item: ImageTransformWorkItem,
        /,
        *,
        messages: MessageReporter = NOOP_MESSAGE_REPORTER,
        progress: ProgressReporter = NOOP_PROGRESS_REPORTER,
    ) -> ImageTransformWorkItem:
        if not item.params.crop or not item.params.crop.enabled:
            messages.info(
                "no_crop_requested",
                "Perspective crop skipped: no crop requested",
                step=self.name,
                image_id=item.image_id,
            )
            return item

        # If corners object exists but contains no points, signal no corners
        if len(item.params.crop.corners) == 0:
            messages.warn(
                "no_quadrat_corners",
                "Perspective crop skipped: no quadrat corners set",
                step=self.name,
                image_id=item.image_id,
            )
            return item

        if not item.params.crop.corners.is_valid():
            messages.warn(
                "invalid_quadrat_corners",
                "Perspective crop skipped: quadrat corners are invalid",
                step=self.name,
                image_id=item.image_id,
                details={"corners": item.params.crop.corners},
            )
            return item

        try:
            progress(0.0, "Computing perspective transform...")
            src = item.image.data
            ordered_corners = np.array(item.params.crop.corners.ordered(), dtype=np.float32)
            tl, tr, br, bl = ordered_corners

            # Compute widths (distance between left and right points) and heights (distance between top and bottom)
            w_bottom = float(np.linalg.norm(br - bl))
            w_top = float(np.linalg.norm(tr - tl))
            h_right = float(np.linalg.norm(tr - br))
            h_left = float(np.linalg.norm(tl - bl))

            # Compute integer target dimensions; ensure at least 1 pixel in each dim.
            tgt_width = max(round(w_bottom), round(w_top), 1)
            tgt_height = max(round(h_right), round(h_left), 1)

            # Destination points: top-left, top-right, bottom-left, bottom-right
            # Use (width-1,height-1) for destination coordinates so they map to valid pixel indices
            tgt_pts = np.array(
                [
                    [0.0, 0.0],
                    [float(max(tgt_width - 1, 0)), 0.0],
                    [0.0, float(max(tgt_height - 1, 0))],
                    [float(max(tgt_width - 1, 0)), float(max(tgt_height - 1, 0))],
                ],
                dtype=np.float32,
            )

            progress(0.5, "Applying perspective transform...")
            M = cv2.getPerspectiveTransform(ordered_corners, tgt_pts)
            dst = cv2.warpPerspective(src, M, (tgt_width, tgt_height))
            progress(1.0)

            return ImageTransformWorkItem(
                image_id=item.image_id,
                image_path=item.image_path,
                image=ImageRGB.from_rgb_array(dst),
                params=item.params,
            )
        except Exception as e:
            messages.error(
                "perspective_crop_failed",
                f"Perspective crop failed: {e!s}",
                step=self.name,
                image_id=item.image_id,
            )
            return item
