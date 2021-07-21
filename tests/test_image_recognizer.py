from app.src.image_recognizer import ImageRecognizer
import unittest
import os


class ImageRecognizerTestCase(unittest.TestCase):
    recognizer: ImageRecognizer

    def setUp(self):
        self.recognizer = ImageRecognizer()
        self.recognizer.is_debug = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')

    def test_recognize(self):
        image_dir = os.path.dirname(os.path.realpath(__file__)) + "/image_recognizer_examples"
        for set_dir in os.listdir(image_dir):
            if not os.path.isdir(image_dir + "/" + set_dir):
                continue

            if set_dir.startswith('is_not_'):
                expected_value = False
                key = 'is_' + set_dir[7:]
            else:
                expected_value = True
                key = set_dir

            if key == 'is_gate_closed':
                # @todo implement is gate closed checks
                continue

            for filename in os.listdir(image_dir + "/" + set_dir):
                image_filepath = image_dir + "/" + set_dir + "/" + filename
                if not os.path.isfile(image_filepath):
                    continue

                if image_filepath[-4:].lower() != '.jpg':
                    print(filename + ' is not JPG file')
                    continue

                with open(image_filepath, "rb") as file:
                    actual_value = self.recognizer.recognize(file.read())[key]

                self.assertEqual(actual_value, expected_value, 'Image detection failed. ' + key + ' is not ' + str(expected_value))
