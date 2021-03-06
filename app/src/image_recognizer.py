import numpy as np
import cv2


class ImageRecognizer:
    is_debug = False

    def recognize(self, raw_image: bytes) -> dict:
        image = cv2.imdecode(np.asarray(bytearray(raw_image), dtype=np.uint8), cv2.IMREAD_COLOR)
        return {
            "is_parking_slot_free": self.check_is_parking_slot_free(image),
            "is_gate_closed": self.check_is_gate_closed(image),
        }

    def check_is_parking_slot_free(self, image: np.ndarray) -> bool:
        image = self.crop_image_part_in_percent(image, 39, 92, 28, 76)
        pixel_percentage = self.count_pixel_percentage(image, [90, 90, 100], [256, 215, 190])

        if self.is_debug:
            print('parking slot fill percentage: ' + str(pixel_percentage))
            cv2.imwrite('storage/result.jpg', image)

        if pixel_percentage > 65:
            return True

        if pixel_percentage < 40:
            return False

        if self.is_debug:
            print(image.shape)

        # try to check is border line visible on image
        border_line_parts = [
            self.crop_image_part_in_percent(image, 10, 11, 38, 39),
            self.crop_image_part_in_percent(image, 20, 21, 27, 28),
            self.crop_image_part_in_percent(image, 3, 4, 48, 49),
        ]

        border_line_parts_founded = 0
        for line_part in border_line_parts:
            if self.count_pixel_percentage(line_part, [190, 185, 190], [230, 230, 250]) == 100:
                border_line_parts_founded += 1

        return border_line_parts_founded > len(border_line_parts) * 0.75

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
        percentage = float(pixel_count / total_pixel_count * 100)

        if self.is_debug:
            print(pixel_count, total_pixel_count, percentage)
            result = cv2.bitwise_and(image, image, mask = ~mask)
            cv2.imwrite('storage/result.jpg', result)
            cv2.imshow('result', result)
            cv2.waitKey(0)

        return percentage

    @staticmethod
    def crop_image_part_in_percent(image: np.ndarray, top: int, bottom: int, left: int, right: int) -> np.ndarray:
        height, width, channels = image.shape
        top = round(top * height * 0.01)
        bottom = round(bottom * height * 0.01)
        left = round(left * width * 0.01)
        right = round(right * width * 0.01)

        return image[top:bottom, left:right]
