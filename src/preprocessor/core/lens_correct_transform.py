from preprocessor.core.image_transform import ImageTransformWorkItem
from preprocessor.core.types import ImageRGB

import cv2
import numpy as np

class LensCorrectTransform:
    name = "lens_correct"

    def __call__(self, item: ImageTransformWorkItem) -> ImageTransformWorkItem:
        if not item.params.lens_correction:
            item.info("no_lens_correction_requested", "Lens correction skipped: no lens correction requested", step=self.name)
            return item

        try:
            src = item.image.data
            h, w = src.shape[:2]

            # Try to obtain camera/distortion parameters
            raw_cam = item.params.lens_correction.camera_matrix or (
                (float(w), 0, float(w) / 2),
                (0, float(w), float(h) / 2),
                (0, 0, 1),
            )
            cam = np.array(raw_cam, dtype=np.float32)
            raw_coeff = item.params.lens_correction.coefficients or [0.0, 0.0, 0.0, 0.0, 0.0]
            coeff = np.array(list(raw_coeff), dtype=np.float32)

            # Compute optimal new camera matrix
            new_cam, _ = cv2.getOptimalNewCameraMatrix(
                cam,
                coeff,
                (w, h),
                1,
            )

            # Build remap matrices
            mapx, mapy = cv2.initUndistortRectifyMap(
                cam,
                coeff,
                None,  # None seems allowed
                new_cam,
                (w, h),
                cv2.CV_32FC1,
            )  # type: ignore[call-overload]

            # Prepare destination image
            dst = np.empty_like(src)

            # Chunked remap to allow cancellation and progress updates
            chunk_h = max(32, min(256, h // 8 if h >= 8 else 1))
            rows_done = 0
            y = 0
            while y < h:
                y1 = min(h, y + chunk_h)
                sub_map1 = mapx[y:y1, :]
                sub_map2 = mapy[y:y1, :]

                remapped = cv2.remap(src, sub_map1, sub_map2, interpolation=cv2.INTER_LINEAR)
                dst[y:y1, ...] = remapped

                rows_done = y1
                y = y1

            return ImageTransformWorkItem(
                image_id=item.image_id,
                image_path=item.image_path,
                image=ImageRGB.from_rgb_array(dst),
                params=item.params,
                messages=item.messages,
            )
        except Exception as e:
            item.error("lens_correction_failed", f"Lens correction failed: {str(e)}", step=self.name)
            return item