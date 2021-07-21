import numpy as np
from PIL import Image
import io
import cv2


class ImageRecognizer:
    is_debug = False

    def recognize(self, raw_image: bytes) -> dict:
        image = cv2.cvtColor(np.array(Image.open(io.BytesIO(raw_image))), cv2.COLOR_RGB2BGR)
        return {
            "is_parking_slot_free": self.check_is_parking_slot_free(image),
            "is_gate_closed": self.check_is_gate_closed(image),
        }

    def check_is_parking_slot_free(self, image: np.ndarray) -> bool:
        image = self.crop_image_part_in_percent(image, 45, 74, 49, 75)
        return self.count_pixel_percentage(image, [90, 90, 100], [175, 175, 190]) > 70

    def check_is_gate_closed(self, image: np.ndarray) -> bool:
        #  @todo implement is gate closed checks
        return True

    def count_pixel_percentage(self, image: np.ndarray, lower_pixel: list, upper_pixel: list) -> float:
        # using .reverse() for convert RGB to BGR
        lower_pixel.reverse()
        upper_pixel.reverse()
        mask = cv2.inRange(image, np.array(lower_pixel), np.array(upper_pixel))

        total_pixel_count = image.shape[0] * image.shape[1]
        pixel_count = int(np.sum(mask == 255))
        percentage = pixel_count / total_pixel_count * 100

        if self.is_debug:
            print(pixel_count, total_pixel_count, percentage)
            result = cv2.bitwise_and(image, image, mask = ~mask)
            cv2.imwrite('result.jpg', result)
            cv2.imshow('result', result)
            cv2.waitKey(0)

        return percentage

    @staticmethod
    def crop_image_part_in_percent(image: np.ndarray, top: int, left: int, bottom: int, right: int) -> np.ndarray:
        height, width, channels = image.shape
        top = round(top * height * 0.01)
        bottom = round(bottom * height * 0.01)
        left = round(left * width * 0.01)
        right = round(right * width * 0.01)

        return image[top:bottom, left:right]
