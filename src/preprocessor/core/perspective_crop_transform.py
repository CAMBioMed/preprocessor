import cv2
import numpy as np

from preprocessor.core.image_transform import ImageTransformWorkItem


class PerspectiveCropTransform:
    name = "perspective_crop"

    def __call__(self, item: ImageTransformWorkItem) -> ImageTransformWorkItem:
        if not item.params.crop:
            item.info("no_crop_requested", "No crop requested; skipping perspective crop", step=self.name)
            return item

        if not item.params.crop.corners:
            item.warn("no_quadrat_corners", "No quadrat corners set; skipping perspective crop", step=self.name)
            return item

        if not item.params.crop.corners.is_valid():
            item.warn("invalid_quadrat_corners", "Quadrat corners are invalid; skipping perspective crop", step=self.name, details={"corners": item.params.crop.corners})
            return item

        try:
            ordered_corners = item.params.crop.corners.ordered()
            tl, tr, bl, br = ordered_corners

            # Compute widths (distance between left and right points) and heights (distance between top and bottom)
            w_bottom = float(np.linalg.norm(br - bl))
            w_top = float(np.linalg.norm(tr - tl))
            h_right = float(np.linalg.norm(tr - br))
            h_left = float(np.linalg.norm(tl - bl))

            # Compute integer target dimensions; ensure at least 1 pixel in each dim.
            tgt_width = max(round(w_bottom), round(w_top), 1)
            tgt_height = max(round(h_right), round(h_left), 1)

            # Destination points: top-left, top-right, bottom-left, bottom-right
            tgt_pts = np.array(
                [
                    [0.0, 0.0],
                    [float(tgt_width), 0.0],
                    [0.0, float(tgt_height)],
                    [float(tgt_width), float(tgt_height)],
                ],
                dtype=np.float32,
            )

            M = cv2.getPerspectiveTransform(ordered_corners, tgt_pts)
            cropped_image = cv2.warpPerspective(item.image, M, (tgt_width, tgt_height))

            return ImageTransformWorkItem(
                image_id=item.image_id,
                image_path=item.image_path,
                image=cropped_image,
                params=item.params,
                messages=item.messages,
            )
        except Exception as e:
            item.error("perspective_crop_failed", f"Perspective crop failed: {e}", step=self.name)
            return item